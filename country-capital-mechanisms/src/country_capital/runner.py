"""Run the same OLMo 3 query with or without activation editing.

Input:
    A loaded model and tokenizer, one tokenized query from ``data.py``, and an
    optional activation-editor callable.
Output:
    Exact generated-answer correctness, gold-answer log-probability metrics,
    generated token IDs, and a small editor-execution audit.

The runner owns model execution and evaluation. It does not define an
intervention. An editor receives each decoder layer's complete activation
tensor and must return a tensor with the same shape, dtype, and device.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Callable, Iterator, Literal

import torch

from .activations import hidden_from_output
from .metrics import completion_metrics


STOP_SEQUENCE = "\n\n"
MAX_NEW_TOKENS = 20

RunPhase = Literal["score", "generate"]
ActivationEditor = Callable[
    [int, torch.Tensor, int, RunPhase],
    torch.Tensor,
]


@contextmanager
def apply_activation_editor(
    model: Any,
    editor: ActivationEditor | None,
    position: int,
) -> Iterator[dict[str, Any]]:
    """Install one hook per decoder layer and always remove every hook.

    Input:
        Model, optional editor, and the fixed prompt-token position to edit.
    Output:
        A mutable audit recording complete scoring and generation forwards.

    The callable interface is ``editor(layer_index, activations, position,
    phase) -> edited_activations``. Passing ``None`` is the baseline condition
    and installs no hooks.
    """
    audit: dict[str, Any] = {
        "editor_active": editor is not None,
        "phase": "score",
        "completed_forwards": {"score": 0, "generate": 0},
    }
    if editor is None:
        yield audit
        return

    layers = model.model.layers
    current_layers: list[int] = []
    handles = []

    def make_hook(layer_index: int):
        def hook(_module: Any, _inputs: Any, output: torch.Tensor) -> torch.Tensor:
            nonlocal current_layers
            activations = hidden_from_output(output)
            if not 0 <= position < activations.shape[1]:
                raise ValueError("editor position is outside the activation sequence")

            if layer_index == 0:
                current_layers = []
            if current_layers != list(range(layer_index)):
                raise RuntimeError("decoder layers did not execute in order")
            current_layers.append(layer_index)

            edited = editor(
                layer_index,
                activations,
                position,
                audit["phase"],
            )
            edited = hidden_from_output(edited)
            if edited.shape != activations.shape:
                raise ValueError("editor changed the activation shape")
            if edited.dtype != activations.dtype:
                raise ValueError("editor changed the activation dtype")
            if edited.device != activations.device:
                raise ValueError("editor changed the activation device")

            if layer_index == len(layers) - 1:
                if current_layers != list(range(len(layers))):
                    raise RuntimeError("not every decoder layer executed")
                audit["completed_forwards"][audit["phase"]] += 1
            return edited

        return hook

    try:
        for layer_index, layer in enumerate(layers):
            handles.append(layer.register_forward_hook(make_hook(layer_index)))
        yield audit
    finally:
        for handle in handles:
            handle.remove()


def run_query(
    model: Any,
    tokenizer: Any,
    query: dict[str, Any],
    activation_editor: ActivationEditor | None = None,
    *,
    max_new_tokens: int = MAX_NEW_TOKENS,
    stop_sequence: str = STOP_SEQUENCE,
) -> dict[str, Any]:
    """Score and greedily generate one answer, optionally editing activations.

    Teacher-forced scoring receives the gold answer prefix. Independent greedy
    generation starts from the original prompt alone. KV caching is disabled so
    the fixed final-prompt position is present and editable on every forward.
    """
    prompt_ids = query["prompt_ids"]
    answer_ids = query["answer_ids"]
    position = query["position"]
    if not prompt_ids or not answer_ids:
        raise ValueError("prompt and answer token IDs must be nonempty")
    if position != len(prompt_ids) - 1:
        raise ValueError("the edited position must be the final prompt token")
    if max_new_tokens < 1:
        raise ValueError("max_new_tokens must be positive")

    device = model.get_input_embeddings().weight.device
    score_input = torch.tensor(
        [prompt_ids + answer_ids[:-1]], dtype=torch.long, device=device
    )
    score_mask = torch.ones_like(score_input)
    prompt_input = torch.tensor([prompt_ids], dtype=torch.long, device=device)
    prompt_mask = torch.ones_like(prompt_input)

    pad_token_id = tokenizer.pad_token_id
    if pad_token_id is None:
        pad_token_id = tokenizer.eos_token_id
    if pad_token_id is None:
        raise ValueError("tokenizer must define a pad or EOS token ID")

    with apply_activation_editor(
        model, activation_editor, position
    ) as editor_audit:
        with torch.inference_mode():
            output = model(
                input_ids=score_input,
                attention_mask=score_mask,
                use_cache=False,
                logits_to_keep=len(answer_ids),
            )
            metrics = completion_metrics(output.logits, answer_ids)
            if activation_editor is not None:
                if editor_audit["completed_forwards"]["score"] != 1:
                    raise RuntimeError("editor did not cover the scoring forward")

            editor_audit["phase"] = "generate"
            generated = model.generate(
                input_ids=prompt_input,
                attention_mask=prompt_mask,
                tokenizer=tokenizer,
                do_sample=False,
                use_cache=False,
                max_new_tokens=max_new_tokens,
                stop_strings=stop_sequence,
                pad_token_id=pad_token_id,
            )
            if activation_editor is not None:
                if editor_audit["completed_forwards"]["generate"] < 1:
                    raise RuntimeError("editor did not cover generation")

    decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
    if not decoded.startswith(query["prompt"]):
        raise RuntimeError("decoded generation does not begin with the original prompt")
    prediction = decoded[len(query["prompt"]) :].split(
        stop_sequence, maxsplit=1
    )[0]

    return {
        **metrics,
        "prediction": prediction,
        "label": query["label"],
        "full_answer_correct": prediction == query["label"],
        "generated_token_ids": generated[0, len(prompt_ids) :].tolist(),
        "editor_audit": {
            "editor_active": editor_audit["editor_active"],
            "completed_forwards": dict(editor_audit["completed_forwards"]),
        },
    }
