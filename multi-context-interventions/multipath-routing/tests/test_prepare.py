from __future__ import annotations

import gzip
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EXPERIMENT_DIR))

from multipath.prepare import (  # noqa: E402
    TaskSource,
    classify_answer,
    create_split,
    prepare_task,
    read_jsonl,
    Entity,
)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if path.suffix == ".gz" else path.open
    kwargs = {"encoding": "utf-8"}
    if path.suffix == ".gz":
        with opener(path, "wt", **kwargs) as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")
    else:
        with opener("w", **kwargs) as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")


def synthetic_source(tmp_path: Path) -> TaskSource:
    source_dir = tmp_path / "source"
    manifest = []
    baseline = []
    routes = [("x0", "A", "Y"), ("x1", "A", "Y"), ("x2", "B", "Z")]
    for query_index, (x, fx, gfx) in enumerate(routes):
        for variant in range(10):
            identifier = f"task__query_{query_index:05d}_context_{variant:02d}"
            context = [{"x": f"demo{variant}-{i}", "Fx": f"D{i}", "GFx": f"O{i}"} for i in range(10)]
            row = {
                "prompt_instance_id": identifier,
                "task": "task",
                "query_index": query_index,
                "context_variant": variant,
                "query": {"x": x, "Fx": fx, "GFx": gfx},
                "context": context,
                "prompt": f"Q: {x}\nA:",
            }
            manifest.append(row)
            prediction = f" {gfx}" if variant % 2 == 0 else " wrong"
            baseline.append(
                {
                    **row,
                    "evaluation": {
                        "prediction": prediction,
                        "label": f" {gfx}",
                        "exact_match": prediction == f" {gfx}",
                    },
                }
            )
    write_jsonl(source_dir / "prompt_manifest.jsonl", manifest)
    write_jsonl(source_dir / "baseline_evaluation.jsonl.gz", baseline)
    (source_dir / "baseline_summary.json").write_text(
        json.dumps(
            {
                "task": "task",
                "model": "model",
                "stage_one_revision": "stage",
                "model_commit": "commit",
                "dtype": "bfloat16",
                "batch_size": 4,
                "max_new_tokens": 20,
                "stop_sequence": "\n\n",
            }
        )
    )
    return TaskSource("task", source_dir, "intermediate_answer_stratified", 10)


class PrepareTests(unittest.TestCase):
    def test_stratified_split_keeps_both_sides_and_is_deterministic(self) -> None:
        entities = [
            Entity(0, "x0", "A", "Y"),
            Entity(1, "x1", "A", "Y"),
            Entity(2, "x2", "A", "Y"),
            Entity(3, "x3", "B", "Z"),
            Entity(4, "x4", "B", "Z"),
            Entity(5, "x5", "C", "W"),
        ]
        first = create_split(entities, "intermediate_answer_stratified", selection_fraction=0.3, seed=0)
        second = create_split(entities, "intermediate_answer_stratified", selection_fraction=0.3, seed=0)
        self.assertEqual(first, second)
        assignment, sizes, singletons = first
        for members in ({"x0", "x1", "x2"}, {"x3", "x4"}):
            self.assertEqual({assignment[x] for x in members}, {"selection", "test"})
        self.assertEqual(sizes["x5"], 1)
        self.assertEqual(singletons, {"x5"})

    def test_answer_status_precedence(self) -> None:
        aliases = {"Washington, D.C.": ["Washington DC"]}
        policy = {"max_words": 4, "reject_multiline": True, "reject_prompt_markers": True, "require_alphanumeric": True}
        self.assertEqual(classify_answer(" Washington, D.C.", " Washington, D.C.", "Washington, D.C.", aliases, policy)["status"], "correct")
        self.assertEqual(classify_answer("Washington DC", " Washington, D.C.", "Washington, D.C.", aliases, policy)["status"], "true_answer_alias")
        self.assertEqual(classify_answer(" Munich", " Berlin", "Berlin", {}, policy)["status"], "eligible_wrong")
        self.assertEqual(classify_answer("Q: next", " Berlin", "Berlin", {}, policy)["reason"], "prompt_spillover")

    def test_prepare_task_preserves_all_records_and_context_groups(self) -> None:
        with TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            source = synthetic_source(tmp_path)
            output = tmp_path / "output"
            summary = prepare_task(
                source,
                output_directory=output,
                aliases={},
                eligibility={"max_words": 12},
                selection_fraction=0.3,
                seed=0,
            )
            rows = list(read_jsonl(output / "prompt_targets.jsonl.gz"))
            self.assertEqual(len(rows), 30)
            self.assertEqual(summary["total_prompts"], 30)
            self.assertEqual(sum(value["prompts"] for value in summary["counts"].values()), 30)
            splits_by_x = {x: {row["split"] for row in rows if row["x"] == x} for x in {"x0", "x1", "x2"}}
            self.assertTrue(all(len(splits) == 1 for splits in splits_by_x.values()))
            self.assertTrue(all(row["num_icl_examples"] == 10 for row in rows))
            self.assertEqual(sum(row["exact_match"] for row in rows), 15)

    def test_prepare_stops_on_incorrect_exact_match_flag(self) -> None:
        with TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            source = synthetic_source(tmp_path)
            rows = list(read_jsonl(source.baseline))
            rows[0]["evaluation"]["exact_match"] = False
            write_jsonl(source.baseline, rows)
            with self.assertRaisesRegex(ValueError, "exact-match flag"):
                prepare_task(
                    source,
                    output_directory=tmp_path / "output",
                    aliases={},
                    eligibility={"max_words": 12},
                )
            self.assertFalse((tmp_path / "output/prompt_targets.jsonl.gz").exists())


if __name__ == "__main__":
    unittest.main()

