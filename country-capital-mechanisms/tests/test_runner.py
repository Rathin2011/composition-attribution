"""CPU tests for shared baseline and activation-edited model execution."""

from __future__ import annotations

from types import SimpleNamespace
import unittest

import torch
from torch import nn

from country_capital.activations import add_to_position
from country_capital.runner import run_query


class TinyTokenizer:
    pad_token_id = 0
    eos_token_id = 3
    pieces = {0: "Q: KV3", 1: "\nA:", 2: " Cairo", 3: " Wrong"}

    def batch_decode(self, rows, skip_special_tokens=True):
        del skip_special_tokens
        return ["".join(self.pieces[int(token)] for token in row) for row in rows]


class TinyCausalModel(nn.Module):
    """A two-layer model whose normal next token is token 2 (`` Cairo``)."""

    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding.from_pretrained(
            torch.tensor([[0.0, 0.0], [2.0, 0.0], [1.0, 0.0], [-1.0, 0.0]])
        )
        self.model = nn.Module()
        self.model.layers = nn.ModuleList([nn.Identity(), nn.Identity()])
        self.lm_head = nn.Linear(2, 4, bias=False)
        with torch.no_grad():
            self.lm_head.weight.copy_(
                torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [-1.0, 0.0]])
            )

    def get_input_embeddings(self):
        return self.embedding

    def forward(
        self, input_ids, attention_mask, use_cache, logits_to_keep
    ):
        self.last_use_cache = use_cache
        del attention_mask
        hidden = self.embedding(input_ids)
        for layer in self.model.layers:
            hidden = layer(hidden)
        logits = self.lm_head(hidden)
        return SimpleNamespace(logits=logits[:, -logits_to_keep:])

    def generate(
        self,
        input_ids,
        attention_mask,
        tokenizer,
        do_sample,
        use_cache,
        max_new_tokens,
        stop_strings,
        pad_token_id,
    ):
        del tokenizer, do_sample, max_new_tokens, stop_strings
        self.last_pad_token_id = pad_token_id
        output = self.forward(
            input_ids=input_ids,
            attention_mask=attention_mask,
            use_cache=use_cache,
            logits_to_keep=1,
        )
        next_token = output.logits[:, -1].argmax(-1, keepdim=True)
        return torch.cat([input_ids, next_token], dim=1)


def tokenized_query():
    return {
        "prompt": "Q: KV3\nA:",
        "label": " Cairo",
        "prompt_ids": [0, 1],
        "answer_ids": [2],
        "position": 1,
    }


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.model = TinyCausalModel().eval()
        self.tokenizer = TinyTokenizer()

    def test_baseline_scores_and_generates_the_complete_answer(self):
        result = run_query(self.model, self.tokenizer, tokenized_query())
        self.assertEqual(result["prediction"], " Cairo")
        self.assertTrue(result["full_answer_correct"])
        self.assertTrue(result["correct_first_token_top1"])
        self.assertEqual(result["generated_token_ids"], [2])
        self.assertEqual(
            result["editor_audit"],
            {
                "editor_active": False,
                "completed_forwards": {"score": 0, "generate": 0},
            },
        )
        self.assertFalse(self.model.last_use_cache)
        self.assertEqual(self.model.last_pad_token_id, 0)

    def test_same_runner_applies_an_editor_during_scoring_and_generation(self):
        calls = []

        def editor(layer_index, activations, position, phase):
            calls.append((phase, layer_index, position, tuple(activations.shape)))
            if layer_index == 0:
                return add_to_position(
                    activations, position, torch.tensor([-4.0, 0.0])
                )
            return activations

        baseline = run_query(self.model, self.tokenizer, tokenized_query())
        changed = run_query(
            self.model,
            self.tokenizer,
            tokenized_query(),
            activation_editor=editor,
        )
        self.assertEqual(changed["prediction"], " Wrong")
        self.assertFalse(changed["full_answer_correct"])
        self.assertLess(changed["completion_logprob"], baseline["completion_logprob"])
        self.assertEqual(
            changed["editor_audit"]["completed_forwards"],
            {"score": 1, "generate": 1},
        )
        self.assertEqual(
            calls,
            [
                ("score", 0, 1, (1, 2, 2)),
                ("score", 1, 1, (1, 2, 2)),
                ("generate", 0, 1, (1, 2, 2)),
                ("generate", 1, 1, (1, 2, 2)),
            ],
        )
        self.assertTrue(all(not layer._forward_hooks for layer in self.model.model.layers))

    def test_hooks_are_removed_when_an_editor_fails(self):
        def failing_editor(layer_index, activations, position, phase):
            del layer_index, activations, position, phase
            raise RuntimeError("deliberate editor failure")

        with self.assertRaisesRegex(RuntimeError, "deliberate editor failure"):
            run_query(
                self.model,
                self.tokenizer,
                tokenized_query(),
                activation_editor=failing_editor,
            )
        self.assertTrue(all(not layer._forward_hooks for layer in self.model.model.layers))


if __name__ == "__main__":
    unittest.main()
