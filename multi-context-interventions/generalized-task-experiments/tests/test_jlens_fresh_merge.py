"""Check the real evaluator-summary/merge boundary without a GPU or repair."""
import contextlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import torch
import evaluate_jlens as evaluator
from merge_jlens_shards import merge_jlens_shards, validate_summaries
from test_evaluate_jlens import eligible_record, FakeLens


class FreshMergeTest(unittest.TestCase):
    def test_fresh_evaluation_merges_without_repair(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.jsonl"
            record = eligible_record()
            source.write_text(json.dumps(record) + "\n")
            shards = root / "shards"
            output = shards / "jlens_shard_001.jsonl.gz"
            summary_path = shards / "jlens_shard_001_summary.json"
            lens_path = root / "fake_lens.pt"
            lens_path.touch()
            args = SimpleNamespace(task=record["task"], input=source,
                catalog_summary=root / "catalog.json", output=output,
                summary_output=summary_path, overwrite=False, lens=lens_path,
                allow_download=False, max_seq_len=512, candidate_chunk_size=16,
                progress_every=10, start_index=0, num_records=1)
            # True Fx has rank 5 at both positions: exercise the old boundary.
            lens = FakeLens({l: torch.tensor([[5., 1., 4., 3., 2.]] * 2)
                             for l in evaluator.EXPECTED_SOURCE_LAYERS})
            lens.n_prompts = 1000
            lens.jacobians = {}
            runtime = SimpleNamespace(JacobianLens=SimpleNamespace(load=lambda _: lens),
                from_hf=lambda *a, **kw: SimpleNamespace(input_device="cpu"))
            catalog = [{"value": "Country", "token_ids": [1]}]
            with contextlib.ExitStack() as stack:
                stack.enter_context(patch.object(evaluator, "parse_args", return_value=args))
                stack.enter_context(patch.object(evaluator, "file_sha256", return_value=evaluator.EXPECTED_LENS_SHA256))
                stack.enter_context(patch.object(evaluator, "_import_runtime", return_value=(runtime, torch, Mock(), Mock())))
                stack.enter_context(patch.object(evaluator, "validate_loaded_lens", return_value=evaluator.EXPECTED_SOURCE_LAYERS))
                stack.enter_context(patch.object(evaluator, "load_fx_catalog", return_value=catalog))
                stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
                evaluator.main()
            summary = json.loads(summary_path.read_text())
            self.assertIn("classification_rank_rule", summary)
            merged = merge_jlens_shards(task=record["task"], source=source,
                shard_directory=shards, output=root / "merged.jsonl.gz",
                summary_output=root / "merged_summary.json")
            self.assertEqual(merged["classification_counts"]["shortcut_candidate"], 1)
            self.assertEqual(merged["classification_rank_rule"], summary["classification_rank_rule"])
            del summary["classification_rank_rule"]
            with self.assertRaisesRegex(ValueError, "missing 'classification_rank_rule'"):
                validate_summaries([output], [summary], task=record["task"])


if __name__ == "__main__":
    unittest.main()
