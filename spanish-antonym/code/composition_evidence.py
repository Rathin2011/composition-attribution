"""Shared reciprocal-rank bands for logit-lens composition evidence."""

from __future__ import annotations

from typing import Literal


COMPOSITION_RR_THRESHOLD = 0.5
SHORTCUT_RR_THRESHOLD = 0.2

EvidenceGroup = Literal["compositional", "ambiguous", "shortcut_candidate"]


def classify_reciprocal_rank(reciprocal_rank: float) -> EvidenceGroup:
    """Assign the strongest intermediate-token rank to an evidence band."""

    if not 0.0 <= reciprocal_rank <= 1.0:
        raise ValueError("reciprocal_rank must be between 0 and 1")
    if reciprocal_rank >= COMPOSITION_RR_THRESHOLD:
        return "compositional"
    if reciprocal_rank <= SHORTCUT_RR_THRESHOLD:
        return "shortcut_candidate"
    return "ambiguous"
