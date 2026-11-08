"""Pure tensor operations for Stage-03 gradient ranking.

This module deliberately contains no model loading, hooks, prompt selection,
or file I/O.  It defines the quantity ranked by the later GPU runner and makes
that quantity testable on small CPU tensors.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import torch


TARGET_MODES = ("true", "model")


def target_answer_for_record(record: Mapping[str, Any], target_mode: str) -> str | None:
    """Resolve the Stage-03 answer target without reinterpreting predictions."""

    if target_mode not in TARGET_MODES:
        raise ValueError(f"unknown target mode: {target_mode}")
    if target_mode == "model" and record.get("answer_status") == "ineligible":
        return None
    field = "true_answer" if target_mode == "true" else "model_answer_normalized"
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"prepared record lacks {field}")
    return " ".join(value.strip().split())


def select_gradient_records(
    records: Iterable[Mapping[str, Any]],
    *,
    task: str,
    split: str,
    target_mode: str,
    association_answers: set[str],
    start_index: int,
    num_prompts: int,
    context_variant: int | None = None,
    skipped: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Select a deterministic shard from the prepared prompt population.

    The start index is defined after task, split, optional context variant,
    target eligibility and association coverage are applied. Missing
    association coverage is an error unless ``skipped`` is a list; then prompts
    whose target has no association row are left out and their IDs appended.
    """

    if split not in {"selection", "test"}:
        raise ValueError("split must be selection or test")
    if start_index < 0 or num_prompts <= 0:
        raise ValueError("start_index must be nonnegative and num_prompts positive")
    selected, eligible_index = [], 0
    seen_ids: set[str] = set()
    for row_number, source in enumerate(records, start=1):
        if source.get("task") != task or source.get("split") != split:
            continue
        if context_variant is not None and source.get("context_variant") != context_variant:
            continue
        identifier = source.get("prompt_instance_id")
        if not isinstance(identifier, str) or not identifier or identifier in seen_ids:
            raise ValueError(f"prepared row {row_number} has an invalid or duplicate prompt ID")
        seen_ids.add(identifier)
        target = target_answer_for_record(source, target_mode)
        if target is None:
            continue
        if target not in association_answers:
            if skipped is None:
                raise ValueError(f"association artifact lacks target answer {target!r}")
            skipped.append(identifier)
            continue
        if eligible_index >= start_index and len(selected) < num_prompts:
            row = dict(source)
            row["gradient_target_mode"] = target_mode
            row["gradient_target_answer"] = target
            selected.append(row)
        eligible_index += 1
        if len(selected) == num_prompts:
            break
    if len(selected) != num_prompts:
        raise ValueError(
            f"requested {num_prompts} prompts at index {start_index}, found {len(selected)}"
        )
    return selected


def full_answer_log_probability(
    answer_logits: torch.Tensor,
    answer_token_ids: Sequence[int],
) -> torch.Tensor:
    """Return the teacher-forced log probability of a complete answer.

    ``answer_logits`` has shape ``[num_answer_tokens, vocab_size]``.  Row
    ``i`` predicts ``answer_token_ids[i]``.  The returned scalar remains
    attached to autograd so a runner can differentiate it with respect to a
    selected hidden state.
    """

    if answer_logits.ndim != 2 or not answer_logits.is_floating_point():
        raise ValueError("answer_logits must be a floating [tokens, vocabulary] tensor")
    if not torch.isfinite(answer_logits).all():
        raise ValueError("answer_logits must contain only finite values")
    if len(answer_token_ids) != answer_logits.shape[0] or not answer_token_ids:
        raise ValueError("one non-empty target token ID is required per logit row")
    targets = torch.as_tensor(answer_token_ids, device=answer_logits.device, dtype=torch.long)
    if bool(((targets < 0) | (targets >= answer_logits.shape[1])).any()):
        raise ValueError("an answer token ID is outside the vocabulary")
    return answer_logits.float().log_softmax(dim=-1).gather(1, targets[:, None]).sum()


def unit_transported_directions(
    jacobian: torch.Tensor,
    readout_rows: torch.Tensor,
) -> torch.Tensor:
    """Return row-wise unit directions ``J_l.T @ w_t``.

    ``jacobian`` is ``[d_model, d_model]`` and maps a layer-local residual
    change to its fitted final-residual change. ``readout_rows`` is
    ``[num_tokens, d_model]``.  In row notation the vectorized calculation is
    ``readout_rows @ jacobian``.

    The caller supplies the exact readout rows used by the experiment.  This
    keeps choices such as applying an RMSNorm gain explicit in the GPU runner
    rather than silently embedding them in this mathematical primitive.
    """

    if jacobian.ndim != 2 or jacobian.shape[0] != jacobian.shape[1]:
        raise ValueError("jacobian must be square")
    if readout_rows.ndim != 2 or readout_rows.shape[1] != jacobian.shape[0]:
        raise ValueError("readout_rows must have shape [num_tokens, d_model]")
    if not jacobian.is_floating_point() or not readout_rows.is_floating_point():
        raise ValueError("jacobian and readout_rows must be floating tensors")
    if not torch.isfinite(jacobian).all() or not torch.isfinite(readout_rows).all():
        raise ValueError("jacobian and readout_rows must contain only finite values")

    work_jacobian = jacobian.detach().float()
    rows = readout_rows.detach().to(device=work_jacobian.device, dtype=torch.float32)
    directions = rows @ work_jacobian
    norms = torch.linalg.vector_norm(directions, dim=1, keepdim=True)
    if bool((norms == 0).any()):
        raise ValueError("a transported vocabulary direction is zero")
    return directions / norms


def directional_gradient_scores(
    gradient: torch.Tensor,
    unit_directions: torch.Tensor,
) -> torch.Tensor:
    """Score infinitesimal positive steering along every supplied direction.

    The score for token ``t`` is ``gradient dot unit_direction[t]``.  A
    positive value predicts that a small positive edit raises the target's
    full-answer log probability; a negative value predicts the opposite.
    """

    if gradient.ndim != 1 or not gradient.is_floating_point():
        raise ValueError("gradient must be a floating [d_model] tensor")
    if unit_directions.ndim != 2 or unit_directions.shape[1] != gradient.shape[0]:
        raise ValueError("unit_directions must have shape [num_tokens, d_model]")
    if not unit_directions.is_floating_point():
        raise ValueError("unit_directions must be floating")
    if not torch.isfinite(gradient).all() or not torch.isfinite(unit_directions).all():
        raise ValueError("gradient and directions must contain only finite values")
    row_norms = torch.linalg.vector_norm(unit_directions.float(), dim=1)
    if not torch.allclose(row_norms, torch.ones_like(row_norms), atol=1e-5, rtol=1e-5):
        raise ValueError("unit_directions rows must have unit norm")
    return unit_directions.float() @ gradient.to(device=unit_directions.device, dtype=torch.float32)


def selected_vocabulary_rankings(
    vocabulary_scores: torch.Tensor,
    token_ids: Sequence[int],
    words: Sequence[str] | None = None,
) -> list[dict[str, Any]]:
    """Return scores and tie-best whole-vocabulary ranks for selected tokens.

    Rank is ``1 + count(score > selected_score)``.  This is the same explicit
    tie convention used elsewhere in the project and avoids dependence on an
    arbitrary sort order.  Ranking is against every row in
    ``vocabulary_scores``; filtering to word tokens, if desired, must happen
    explicitly in the runner and be recorded as a separate measurement.
    """

    if vocabulary_scores.ndim != 1 or not vocabulary_scores.is_floating_point():
        raise ValueError("vocabulary_scores must be a floating [vocabulary] tensor")
    if not torch.isfinite(vocabulary_scores).all():
        raise ValueError("vocabulary_scores must contain only finite values")
    ids = [int(token_id) for token_id in token_ids]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError("token_ids must be non-empty and unique")
    if any(token_id < 0 or token_id >= vocabulary_scores.shape[0] for token_id in ids):
        raise ValueError("a selected token ID is outside the vocabulary")
    if words is not None and len(words) != len(ids):
        raise ValueError("words must align one-to-one with token_ids")

    scores = vocabulary_scores.float()
    output = []
    for index, token_id in enumerate(ids):
        score = scores[token_id]
        rank = 1 + int((scores > score).sum().item())
        row: dict[str, Any] = {
            "token_id": token_id,
            "directional_score": float(score.item()),
            "full_vocabulary_rank": rank,
            "full_vocabulary_percentile": 1.0 - ((rank - 1) / max(1, scores.numel() - 1)),
            "predicted_effect": "increase" if score > 0 else "decrease" if score < 0 else "neutral",
        }
        if words is not None:
            row["word"] = words[index]
        output.append(row)
    return output
