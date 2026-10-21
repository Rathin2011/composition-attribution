import copy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from evaluate_hop_filters import dataset_index, hop_prompt, required_hops, write_populations
from evaluate_baseline import read_jsonl


class HopFilterTests(unittest.TestCase):
    task = "landmark-country-capital"

    def fixtures(self):
        query = dict(x="KV3", Fx="Egypt", GFx="Cairo")
        context = dict(x="Mount Fuji", Fx="Japan", GFx="Tokyo")
        index = dataset_index([dict(task=self.task, **r) for r in (query, context)], self.task)
        record = dict(prompt_instance_id="q0_c0", task=self.task, query=query,
                      context=[context], prompt="Q: Mount Fuji\nA: Tokyo\n\nQ: KV3\nA:",
                      evaluation=dict(exact_match=True))
        return record, index

    def test_hop_prompts_reuse_context(self):
        record, index = self.fixtures()
        self.assertEqual(hop_prompt(record, index, self.task, "Fx", "GFx"),
                         ("Q: Japan\nA: Tokyo\n\nQ: Egypt\nA:", " Cairo"))

    def test_populations_and_audit(self):
        record, index = self.fixtures()
        second = copy.deepcopy(record)
        second["prompt_instance_id"] = "q0_c1"
        wrong = copy.deepcopy(record)
        wrong["prompt_instance_id"] = "q1_c0"
        wrong["evaluation"]["exact_match"] = False
        answers = iter([" Egypt", " Cairo", " Egypt", " Tokyo"])
        with TemporaryDirectory() as directory:
            root = Path(directory)
            summary = write_populations(records=[record, second, wrong], task=self.task,
                index=index, predict=lambda _: next(answers), output_root=root, provenance={})
            self.assertEqual(summary["composition_correct"], 2)
            self.assertEqual(summary["all_hops_and_composition_correct"], 1)
            self.assertEqual(list(read_jsonl(root / "composition_correct/correct_instances.jsonl.gz")), [record, second])
            self.assertEqual(list(read_jsonl(root / "all_hops_and_composition_correct/correct_instances.jsonl.gz")), [record])
            audit = list(read_jsonl(root / "hop_evaluation.jsonl.gz"))
            self.assertEqual(len(audit), 2)
            self.assertFalse(audit[1]["hops"][1]["exact_match"])

    def test_alternative_route_numeric_labels(self):
        task = "plus-ten-times-two"
        row = dict(task=task, x="5", Fx="15", Gx="10", GFx="30")
        index = dataset_index([row], task)
        record = dict(query={k: row[k] for k in ("x", "Fx", "GFx")}, context=[])
        self.assertEqual(len(required_hops(task)), 4)
        self.assertEqual(hop_prompt(record, index, task, "x", "Gx"), ("Q: 5\nA: ", "10"))
        self.assertEqual(hop_prompt(record, index, task, "Gx", "GFx"), ("Q: 10\nA: ", "30"))

    def test_missing_gx_and_mismatched_dataset_rejected(self):
        with self.assertRaises(ValueError):
            dataset_index([dict(task="antonym-spanish", x="good", Fx="bad", GFx="malo")], "antonym-spanish")
        record, index = self.fixtures()
        record["query"]["Fx"] = "Italy"
        with self.assertRaises(ValueError):
            hop_prompt(record, index, self.task, "x", "Fx")

    def test_duplicate_instances_do_not_publish_results(self):
        record, index = self.fixtures()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                write_populations(records=[record, record], task=self.task, index=index,
                    predict=lambda _: "wrong", output_root=root, provenance={})
            self.assertFalse((root / "filtering_summary.json").exists())
            self.assertFalse(list(root.rglob("*.gz")))


if __name__ == "__main__":
    unittest.main()
