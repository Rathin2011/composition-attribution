from pathlib import Path
import tempfile
import unittest

import build_stage1_inventory as inventory
from stage1_data import ManifestEntry, TOKEN_BYTES, TRAIN_SEQUENCE_LENGTH


class FakeResponse:
    def __init__(self, content_length: str | None):
        self.headers = {}
        if content_length is not None:
            self.headers["Content-Length"] = content_length

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class BuildStageOneInventoryTest(unittest.TestCase):
    def test_get_remote_file_size_uses_head_content_length(self) -> None:
        def fake_opener(request: object, *, timeout: float) -> FakeResponse:
            self.assertEqual(request.get_method(), "HEAD")
            self.assertEqual(timeout, 12.0)
            return FakeResponse("131072")

        size = inventory.get_remote_file_size(
            "https://example.test/shard.npy", timeout=12.0, opener=fake_opener
        )
        self.assertEqual(size, 131_072)

    def test_get_remote_file_size_requires_content_length(self) -> None:
        def fake_opener(request: object, *, timeout: float) -> FakeResponse:
            return FakeResponse(None)

        with self.assertRaisesRegex(ValueError, "did not provide Content-Length"):
            inventory.get_remote_file_size(
                "https://example.test/shard.npy", opener=fake_opener
            )

    def test_summarize_shard_counts_complete_sequences(self) -> None:
        entry = ManifestEntry("source", "relative.npy", "https://example.test/shard.npy")
        byte_size = TOKEN_BYTES * (3 * TRAIN_SEQUENCE_LENGTH + 17)

        result = inventory.summarize_shard(entry, byte_size)

        self.assertEqual(result.token_count, 3 * TRAIN_SEQUENCE_LENGTH + 17)
        self.assertEqual(result.complete_train_sequences, 3)
        self.assertEqual(result.trailing_tokens, 17)

    def test_summarize_shard_rejects_partial_token(self) -> None:
        entry = ManifestEntry("source", "relative.npy", "https://example.test/shard.npy")
        with self.assertRaisesRegex(ValueError, "not divisible"):
            inventory.summarize_shard(entry, TOKEN_BYTES + 1)

    def test_retry_repeats_transient_failure(self) -> None:
        calls = 0

        def flaky_size_getter(url: str, timeout: float) -> int:
            nonlocal calls
            calls += 1
            if calls < 3:
                raise TimeoutError("temporary")
            return 100

        size = inventory.get_file_size_with_retries(
            "https://example.test/shard.npy",
            12.0,
            3,
            size_getter=flaky_size_getter,
            sleeper=lambda seconds: None,
        )
        self.assertEqual(size, 100)
        self.assertEqual(calls, 3)

    def test_inspect_all_shards_preserves_manifest_order(self) -> None:
        entries = [
            ManifestEntry("first", "first.npy", "https://example.test/first.npy"),
            ManifestEntry("second", "second.npy", "https://example.test/second.npy"),
        ]
        sizes = {
            entries[0].url: TOKEN_BYTES * TRAIN_SEQUENCE_LENGTH,
            entries[1].url: TOKEN_BYTES * 2 * TRAIN_SEQUENCE_LENGTH,
        }

        results = inventory.inspect_all_shards(
            entries,
            timeout=12.0,
            max_workers=2,
            retries=1,
            size_getter=lambda url, timeout: sizes[url],
            verbose=False,
        )

        self.assertEqual([result.source for result in results], ["first", "second"])

    def test_payload_assigns_offsets_and_checks_batch_count(self) -> None:
        entries = [
            ManifestEntry("first", "first.npy", "https://example.test/first.npy"),
            ManifestEntry("second", "second.npy", "https://example.test/second.npy"),
        ]
        inspections = [
            inventory.summarize_shard(
                entries[0], TOKEN_BYTES * 512 * TRAIN_SEQUENCE_LENGTH
            ),
            inventory.summarize_shard(
                entries[1], TOKEN_BYTES * 3 * TRAIN_SEQUENCE_LENGTH
            ),
        ]

        payload = inventory.build_inventory_payload(
            inspections, expected_stage_one_steps=1
        )

        shards = payload["shards"]
        self.assertEqual(shards[0]["sequence_start"], 0)
        self.assertEqual(shards[0]["sequence_end"], 512)
        self.assertEqual(shards[1]["sequence_start"], 512)
        self.assertEqual(shards[1]["sequence_end"], 515)
        self.assertEqual(payload["final_incomplete_batch_sequences"], 3)

    def test_save_inventory_writes_json_atomically(self) -> None:
        payload = {"schema_version": 1, "shards": []}
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "inventory.json"
            saved = inventory.save_inventory(payload, output)

            self.assertEqual(saved, output)
            self.assertEqual(output.read_text(encoding="utf-8"), '{\n  "schema_version": 1,\n  "shards": []\n}\n')
            self.assertFalse((output.parent / ".inventory.json.tmp").exists())


if __name__ == "__main__":
    unittest.main()
