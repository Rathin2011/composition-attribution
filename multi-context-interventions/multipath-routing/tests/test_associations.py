from __future__ import annotations

import gzip
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import torch

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EXPERIMENT_DIR))

from multipath.associations import (GenerationSpec, build_candidate_pool, build_target_inventory,
    finalize_associations, leave_one_out_contrast, load_static_catalog,
    parse_generated_candidates, single_token_word)


class FakeTokenizer:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [self.tokens.index(text)] if text in self.tokens else [98, 99]
    def decode(self, ids: list[int]) -> str:
        return self.tokens[ids[0]]


def spec(top_n: int = 2, k_values: tuple[int, ...] | None = None,
         primary_k: int | None = None) -> GenerationSpec:
    if k_values is None:
        k_values = (1,) if top_n == 1 else (1, 2)
    if primary_k is None:
        primary_k = k_values[-1]
    return GenerationSpec(
        task="task", answer_type="city",
        templates=("{answer} {count}", "x {answer} {count}"),
        scoring_templates=("{answer} one", "x {answer} two"),
        top_n=top_n, analysis_k_values=k_values, primary_k=primary_k,
        requested_candidates=5, max_new_tokens=20,
        stopwords=frozenset({"city"}),
        generic_capital_words=frozenset({"government"}),
        excluded_generic_name_pieces=frozenset({"white"}),
        generic_min_answers=1, generic_max_answer_fraction=0.25,
        provider="test",
    )


class AssociationTests(unittest.TestCase):
    def test_inventory_records_complete_task_intermediate_catalog(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "prepared.jsonl.gz"
            model = {"model": "m", "model_commit": "c", "dtype": "bfloat16"}
            rows = [
                {"task": "task", "split": "selection", "true_answer": "Berlin", "model_answer_normalized": "Berlin",
                 "answer_status": "correct", "x": "gate", "Fx": "Germany", "model": model},
                {"task": "task", "split": "test", "true_answer": "Paris", "model_answer_normalized": "Lyon",
                 "answer_status": "eligible_wrong", "x": "tower", "Fx": "France", "model": model},
            ]
            with gzip.open(path, "wt", encoding="utf-8") as handle:
                for row in rows: handle.write(json.dumps(row) + "\n")
            inventory = build_target_inventory(path, "task", "city")
            self.assertEqual(inventory["task_intermediates"], ["France", "Germany"])
            self.assertEqual({row["answer"] for row in inventory["modes"]["model"]}, {"Berlin", "Lyon"})

    def test_parser_accepts_only_explicit_list_words(self) -> None:
        self.assertEqual(parse_generated_candidates("museum, 2. river; royal palace\nart"),
                         ["museum", "river", "art"])

    def test_single_token_validation_uses_leading_space_token(self) -> None:
        tokenizer = FakeTokenizer([" museum", " river"])
        self.assertEqual(single_token_word(tokenizer, "museum"), (0, "museum"))
        self.assertIsNone(single_token_word(tokenizer, "royal palace"))

    def test_pool_excludes_answer_and_every_task_intermediate(self) -> None:
        tokenizer = FakeTokenizer([" Berlin", " Germany", " France", " government", " white", " museum", " river", " city"])
        target = {"answer": "Berlin"}
        pool, intermediates, capital_words, name_pieces, rejected = build_candidate_pool(
            tokenizer=tokenizer, target=target,
            generations=["Berlin, Germany, France, government, white, museum, river, city", "museum, river"],
            task_intermediates=["Germany", "France"], aliases=[], spec=spec())
        self.assertEqual([row["text"] for row in pool], ["museum", "river"])
        self.assertEqual({row["text"] for row in intermediates}, {"Germany", "France"})
        self.assertEqual([row["text"] for row in capital_words], ["government"])
        self.assertEqual([row["text"] for row in name_pieces], ["white"])
        self.assertEqual(rejected["answer_or_answer_piece"], 1)
        self.assertEqual(rejected["task_intermediate_or_piece"], 2)

    def test_merge_filters_generic_words_and_is_deterministic(self) -> None:
        rows = [
            {"target_id": "a", "candidate_pool": [
                {"text": "common", "token_id": 1, "generation_count": 2, "cue_indices": [0], "first_seen": 1},
                {"text": "alpha", "token_id": 2, "generation_count": 1, "cue_indices": [0], "first_seen": 2}]},
            {"target_id": "b", "candidate_pool": [
                {"text": "common", "token_id": 1, "generation_count": 2, "cue_indices": [0], "first_seen": 1},
                {"text": "beta", "token_id": 3, "generation_count": 1, "cue_indices": [0], "first_seen": 2}]},
        ]
        output, audit = finalize_associations(rows, spec(top_n=1))
        self.assertEqual([row["associations"][0]["text"] for row in output], ["alpha", "beta"])
        self.assertEqual(audit["generic_document_frequency_limit"], 1)

    def test_subsets_prefer_specific_words_and_are_nested(self) -> None:
        rows = [
            {"target_id": "a", "candidate_pool": [
                {"text": "shared", "token_id": 1, "generation_count": 1,
                 "cue_indices": [0], "first_seen": 1},
                {"text": "rare", "token_id": 2, "generation_count": 1,
                 "cue_indices": [0], "first_seen": 2}]},
            {"target_id": "b", "candidate_pool": [
                {"text": "shared", "token_id": 1, "generation_count": 1,
                 "cue_indices": [0], "first_seen": 1}]},
        ]
        output, audit = finalize_associations(
            rows, spec(top_n=2, k_values=(1, 2), primary_k=1), filter_generic=False)
        self.assertEqual([item["text"] for item in output[0]["associations"]], ["rare", "shared"])
        self.assertEqual(output[0]["association_subsets"]["1"]["words"], ["rare"])
        self.assertEqual(output[0]["association_subsets"]["2"]["words"], ["rare", "shared"])
        self.assertTrue(output[0]["association_subsets"]["1"]["is_primary"])
        self.assertEqual(audit["k_coverage"], {"1": 2, "2": 1})

    def test_static_catalog_can_inherit_and_extend_another_task(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps({"schema_version": 1, "tasks": {
                "parent": {"true": {"Shared": ["one", "two"]}},
                "child": {"inherit_from": "parent", "true": {"New": ["three"]}},
            }}), encoding="utf-8")
            self.assertEqual(load_static_catalog(path, "child", "true"), {
                "Shared": ["one", "two"], "New": ["three"]})

    def test_leave_one_out_contrast_excludes_the_target_answer(self) -> None:
        target = torch.tensor([4.0, 2.0])
        # Mean of target [4,2] and two other answers [1,2], [1,5].
        mean = torch.tensor([2.0, 3.0])
        self.assertTrue(torch.allclose(
            leave_one_out_contrast(target, mean, 3), torch.tensor([3.0, -1.5])))


if __name__ == "__main__":
    unittest.main()
