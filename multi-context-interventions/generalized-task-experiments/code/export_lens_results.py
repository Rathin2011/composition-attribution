"""Export merged lens measurements in the requested experiment schema.

The exporter is task-general.  It reads one task's candidate catalog and
merged J-Lens results, emits one ``results_lenses`` entry for every paper-token
eligible prompt instance, and leaves ``results_intervention`` empty until the
intervention stage is run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from evaluate_baseline import read_jsonl
from results import write_results
from tasks import TASKS, get_task_spec


PROJECT_DIR = Path(__file__).resolve().parent.parent


def load_catalog(path: Path, *, task: str) -> tuple[list[str], list[str], list[str]]:
    """Load all possible x, Fx, and GFx values in their canonical order."""

    summary = json.loads(path.read_text(encoding="utf-8"))
    if summary.get("task") != task:
        raise ValueError("candidate catalog task does not match requested task")
    catalog = summary.get("candidate_catalog")
    if not isinstance(catalog, Mapping):
        raise ValueError("baseline summary lacks candidate_catalog")
    x = catalog.get("x")
    fx_rows = catalog.get("Fx")
    gfx_rows = catalog.get("GFx")
    if not isinstance(x, list) or not all(isinstance(value, str) for value in x):
        raise ValueError("candidate x catalog must be a string list")
    for name, rows in (("Fx", fx_rows), ("GFx", gfx_rows)):
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"candidate {name} catalog must be nonempty")
        if any(not isinstance(row, Mapping) or not isinstance(row.get("value"), str) for row in rows):
            raise ValueError(f"candidate {name} entries must contain string values")
    return (
        list(x),
        [row["value"] for row in fx_rows],
        [row["value"] for row in gfx_rows],
    )


def render_icl_context(context: Sequence[Mapping[str, Any]]) -> str:
    """Render demonstrations as ``x->GFx`` pairs separated by semicolons."""

    pairs = []
    for index, example in enumerate(context):
        x = example.get("x")
        gfx = example.get("GFx")
        if not isinstance(x, str) or not isinstance(gfx, str):
            raise ValueError(f"context entry {index} lacks string x/GFx")
        pairs.append(f"{x}->{gfx}")
    if not pairs:
        raise ValueError("ICL context must not be empty")
    return ";".join(pairs)


def lens_records(
    path: Path,
    *,
    task: str,
    expected_fx: int,
) -> Iterator[dict[str, Any]]:
    """Yield requested lens records, omitting paper-filter-excluded rows."""

    seen: set[str] = set()
    for line_number, record in enumerate(read_jsonl(path), start=1):
        if record.get("task") != task:
            raise ValueError(f"lens row {line_number} belongs to another task")
        prompt_id = record.get("prompt_instance_id")
        if not isinstance(prompt_id, str) or prompt_id in seen:
            raise ValueError(f"invalid or duplicate prompt ID on row {line_number}")
        seen.add(prompt_id)
        llens = record.get("logit_lens")
        jlens = record.get("j_lens")
        if not isinstance(llens, Mapping) or not isinstance(jlens, Mapping):
            raise ValueError(f"lens row {line_number} lacks both lens outputs")
        if llens.get("paper_token_eligible") != jlens.get("paper_token_eligible"):
            raise ValueError(f"lens row {line_number} has inconsistent eligibility")
        if not jlens["paper_token_eligible"]:
            continue
        query = record.get("query")
        context = record.get("context")
        if not isinstance(query, Mapping) or not isinstance(context, list):
            raise ValueError(f"lens row {line_number} lacks query/context")
        if len(llens.get("llens_z", [])) != expected_fx or len(
            jlens.get("jlens_z", [])
        ) != expected_fx:
            raise ValueError(f"lens row {line_number} has incomplete Fx logits")
        yield {
            "x": query["x"],
            "Fx": query["Fx"],
            "GFx": query["GFx"],
            "icl_ctx": render_icl_context(context),
            "llens_z": llens["llens_z"],
            "jlens_z": jlens["jlens_z"],
            "llens_rr": llens["llens_rr"],
            "jlens_rr": jlens["jlens_rr"],
            "llens_classification": llens["classification"]["group"],
            "jlens_classification": jlens["classification"]["group"],
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--catalog-summary", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--max-lens-records",
        type=int,
        help="Write only the first N eligible records, for a readable preview.",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    input_path = args.input or task_directory / "jlens_evaluation.jsonl.gz"
    catalog_path = args.catalog_summary or task_directory / "baseline_summary.json"
    output_path = args.output or task_directory / "experiment_results.json"
    if output_path.exists() and not args.overwrite:
        raise FileExistsError(f"output exists; use --overwrite: {output_path}")

    x, fx, gfx = load_catalog(catalog_path, task=task)
    records = lens_records(
        input_path,
        task=task,
        expected_fx=len(fx),
    )
    if args.max_lens_records is not None:
        if args.max_lens_records <= 0:
            raise ValueError("max-lens-records must be positive")
        from itertools import islice

        records = islice(records, args.max_lens_records)
    write_results(
        output_path,
        x=x,
        Fx=fx,
        GFx=gfx,
        results_lenses=records,
        results_intervention=[],
    )
    print(
        json.dumps(
            {
                "task": task,
                "input": str(input_path),
                "output": str(output_path),
                "n_x": len(x),
                "n_Fx": len(fx),
                "n_GFx": len(gfx),
                "results_intervention": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
