"""Load and validate saved landmark–country–capital experiment inputs.

The saved JSONL files already contain the behavioral answer and logit-lens
classification. This module checks that provenance rather than recomputing or
changing the classification.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import MODEL_COMMIT, MODEL_ID, MODEL_REVISION


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read every non-empty JSON object from ``path`` without modifying it."""
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def reconstruct_prompt(context: list[dict[str, Any]], landmark: str) -> str:
    """Reconstruct the exact ten-example landmark-to-capital ICL prompt."""
    demonstrations = "".join(
        f"Q: {example['x']}\nA: {example['GFx']}\n\n" for example in context
    )
    return f"{demonstrations}Q: {landmark}\nA:"


def validate_compositional_queries(
    records: list[dict[str, Any]], *, expected_count: int | None = 370
) -> list[dict[str, Any]]:
    """Validate and normalize saved compositional-query rows.

    This preserves the completed experiment's definition: the direct
    landmark-to-capital answer must be exactly correct, the saved group must be
    ``compositional``, and the intermediate-country peak reciprocal rank must
    be at least 0.5. No query is reclassified here.
    """
    if expected_count is not None and len(records) != expected_count:
        raise ValueError(
            f"expected {expected_count} compositional rows, found {len(records)}"
        )
    if not records:
        raise ValueError("at least one compositional row is required")

    normalized: list[dict[str, Any]] = []
    indices: set[int] = set()
    for source in records:
        index = source["evaluation_index"]
        if not isinstance(index, int) or isinstance(index, bool) or index in indices:
            raise ValueError("evaluation indices must be unique integers")
        indices.add(index)

        identity = (
            source.get("model"),
            source.get("model_commit"),
            source.get("stage_one_revision"),
        )
        if identity != (MODEL_ID, MODEL_COMMIT, MODEL_REVISION):
            raise ValueError(f"checkpoint mismatch at evaluation {index}")

        query = source["query"]
        prediction = source["prediction"]
        evidence = source["node_evidence"]["Fx"]
        classification = source["classification"]
        label = f" {query['GFx']}"

        if prediction["pred"] != prediction["label"] or prediction["label"] != label:
            raise ValueError(f"source answer is not exactly correct at evaluation {index}")
        if len(source["context"]) != 10:
            raise ValueError(f"expected ten context examples at evaluation {index}")
        if prediction["prompt"] != reconstruct_prompt(source["context"], query["x"]):
            raise ValueError(f"original prompt/context mismatch at evaluation {index}")
        if (
            classification["group"] != "compositional"
            or evidence["value"] != query["Fx"]
            or evidence["peak_reciprocal_rank"] < 0.5
            or classification["best_vocabulary_rank"]
            != evidence["best_vocabulary_rank"]
            or classification["peak_reciprocal_rank"]
            != evidence["peak_reciprocal_rank"]
        ):
            raise ValueError(f"invalid composition evidence at evaluation {index}")

        normalized.append(
            {
                "evaluation_index": index,
                "landmark": query["x"],
                "country": query["Fx"],
                "capital": query["GFx"],
                "prompt": prediction["prompt"],
                "label": prediction["label"],
                "original_prediction": prediction["pred"],
                "context": source["context"],
                "original_country_evidence": evidence,
            }
        )
    return normalized


def load_compositional_queries(
    path: Path, *, expected_count: int | None = 370
) -> list[dict[str, Any]]:
    """Read and validate the saved compositional-query JSONL file."""
    return validate_compositional_queries(
        read_jsonl(path), expected_count=expected_count
    )


def tokenize_queries(
    rows: list[dict[str, Any]], tokenizer: Any
) -> list[dict[str, Any]]:
    """Attach prompt, answer, and first-country token IDs to validated rows."""
    tokenized: list[dict[str, Any]] = []
    for row in rows:
        prompt_ids = tokenizer.encode(row["prompt"], add_special_tokens=False)
        answer_ids = tokenizer.encode(row["label"], add_special_tokens=False)
        country_ids = tokenizer.encode(f" {row['country']}", add_special_tokens=False)
        if not prompt_ids or not answer_ids or not country_ids:
            raise ValueError("prompt, country, and answer must tokenize to nonempty sequences")
        combined = tokenizer.encode(
            row["prompt"] + row["label"], add_special_tokens=False
        )
        if combined != prompt_ids + answer_ids:
            raise ValueError(
                f"token boundary mismatch at evaluation {row['evaluation_index']}"
            )
        if country_ids[0] != row["original_country_evidence"]["first_token_id"]:
            raise ValueError(
                f"saved country token mismatch at evaluation {row['evaluation_index']}"
            )

        final_prompt_position = len(prompt_ids) - 1
        peak_locations = row["original_country_evidence"]["peak_locations"]
        tokenized.append(
            {
                **row,
                "prompt_ids": prompt_ids,
                "answer_ids": answer_ids,
                "country_id": country_ids[0],
                "position": final_prompt_position,
                "original_peak_includes_final_position": any(
                    location["prompt_position"] == final_prompt_position
                    for location in peak_locations
                ),
            }
        )
    return tokenized
