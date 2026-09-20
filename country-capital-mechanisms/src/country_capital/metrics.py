"""Downstream answer-scoring helpers shared by causal experiments."""

from __future__ import annotations

import torch


def completion_metrics(logits: torch.Tensor, completion_ids: list[int]) -> dict:
    """Score every teacher-forced answer token and the first greedy prediction.

    The returned completion score is a summed sequence log-probability, not an
    average token loss. It does not score any in-context demonstrations.
    """
    if (
        not completion_ids
        or logits.ndim != 3
        or logits.shape[0] != 1
        or logits.shape[1] < len(completion_ids)
    ):
        raise ValueError("logits must cover every completion token for one prompt")

    scores = logits[0, -len(completion_ids) :].float()
    targets = torch.tensor(completion_ids, device=scores.device)
    token_logprobs = scores.log_softmax(dim=-1).gather(1, targets[:, None]).squeeze(1)
    first_prediction = scores[0].argmax().item()
    return {
        "completion_logprob": token_logprobs.sum().item(),
        "completion_token_logprobs": token_logprobs.cpu().tolist(),
        "greedy_next_token_id": first_prediction,
        "correct_first_token_top1": first_prediction == completion_ids[0],
    }
