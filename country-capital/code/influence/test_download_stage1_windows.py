from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

import download_stage1_windows as download


class FakeResponse:
    def __init__(
        self,
        raw_bytes: bytes,
        *,
        status: int = 206,
        content_range: str | None = None,
    ):
        self.status = status
        self.headers = {}
        if content_range is not None:
            self.headers["Content-Range"] = content_range
        self.raw_bytes = raw_bytes

    def getcode(self) -> int:
        return self.status

    def read(self) -> bytes:
        return self.raw_bytes

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class DownloadStageOneWindowsTest(unittest.TestCase):
    def test_cohort_configs_are_separate_and_have_expected_sizes(self) -> None:
        hessian = download.COHORTS["hessian"]
        ranking = download.COHORTS["ranking"]
        self.assertEqual(hessian.expected_count, 10_000)
        self.assertEqual(ranking.expected_count, 100_000)
        self.assertNotEqual(hessian.samples_path, ranking.samples_path)
        self.assertNotEqual(hessian.tokens_path, ranking.tokens_path)
        self.assertNotEqual(hessian.summary_path, ranking.summary_path)

    def test_fetch_byte_range_sets_and_validates_exact_range(self) -> None:
        raw_bytes = bytes(range(8))

        def fake_opener(request: object, *, timeout: float) -> FakeResponse:
            self.assertEqual(request.get_header("Range"), "bytes=20-27")
            self.assertEqual(timeout, 12.0)
            return FakeResponse(raw_bytes, content_range="bytes 20-27/100")

        result = download.fetch_byte_range(
            "https://example.test/shard.npy",
            20,
            28,
            timeout=12.0,
            opener=fake_opener,
        )
        self.assertEqual(result, raw_bytes)

    def test_fetch_byte_range_rejects_full_file_response(self) -> None:
        def fake_opener(request: object, *, timeout: float) -> FakeResponse:
            return FakeResponse(b"full file", status=200)

        with self.assertRaisesRegex(ValueError, "not partial-content"):
            download.fetch_byte_range(
                "https://example.test/shard.npy", 20, 28, opener=fake_opener
            )

    def test_fetch_byte_range_rejects_wrong_content_range(self) -> None:
        def fake_opener(request: object, *, timeout: float) -> FakeResponse:
            return FakeResponse(b"12345678", content_range="bytes 21-28/100")

        with self.assertRaisesRegex(ValueError, "wrong byte range"):
            download.fetch_byte_range(
                "https://example.test/shard.npy", 20, 28, opener=fake_opener
            )

    def test_bytes_to_token_ids_decodes_512_uint32_values(self) -> None:
        expected = np.arange(512, dtype="<u4")
        actual = download.bytes_to_token_ids(expected.tobytes())
        np.testing.assert_array_equal(actual, expected)

    def test_inspect_first_download_prints_realized_counts(self) -> None:
        token_bytes = np.arange(512, dtype="<u4").tobytes()

        def fake_fetcher(
            url: str, byte_start: int, byte_end: int, *, timeout: float
        ) -> bytes:
            self.assertEqual(url, "https://example.test/shard.npy")
            self.assertEqual((byte_start, byte_end), (100, 2148))
            return token_bytes

        record = {
            "url": "https://example.test/shard.npy",
            "source": "test_source",
            "manifest_index": 7,
            "byte_start": 100,
            "byte_end": 2148,
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "samples.jsonl"
            path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                result = download.inspect_first_download(
                    path, timeout=12.0, range_fetcher=fake_fetcher
                )

        self.assertEqual(len(result), 512)
        self.assertIn("Bytes received: 2,048", output.getvalue())
        self.assertIn("Token IDs received: 512", output.getvalue())
        self.assertIn("First 20 token IDs", output.getvalue())

    def test_download_cohort_preserves_sample_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            records = [
                {
                    "cohort": "test",
                    "sample_index": index,
                    "global_window_id": index + 10,
                    "url": f"https://example.test/{index}.npy",
                    "source": "source",
                    "manifest_index": index,
                    "byte_start": index * 2048,
                    "byte_end": (index + 1) * 2048,
                }
                for index in range(3)
            ]
            samples_path = directory / "samples.jsonl"
            samples_path.write_text(
                "".join(json.dumps(record) + "\n" for record in records),
                encoding="utf-8",
            )
            config = download.CohortConfig(
                name="test",
                samples_path=samples_path,
                expected_count=3,
                tokens_path=directory / "tokens.npy",
                summary_path=directory / "summary.json",
            )

            def fake_fetcher(
                url: str, byte_start: int, byte_end: int, *, timeout: float
            ) -> bytes:
                row = byte_start // 2048
                return np.full(512, row, dtype="<u4").tobytes()

            summary = download.download_cohort(
                config,
                max_workers=2,
                retries=1,
                progress_interval=1,
                range_fetcher=fake_fetcher,
            )
            tokens = np.load(config.tokens_path)

            self.assertEqual(tokens.shape, (3, 512))
            np.testing.assert_array_equal(tokens[:, 0], np.array([0, 1, 2]))
            self.assertEqual(summary["cohort"], "test")
            self.assertEqual(summary["records"], 3)
            self.assertTrue(config.summary_path.is_file())
            partial_tokens, completion_bitmap = download.progress_paths(
                config.tokens_path
            )
            self.assertFalse(partial_tokens.exists())
            self.assertFalse(completion_bitmap.exists())

    def test_download_cohort_resumes_completed_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            records = [
                {
                    "cohort": "test",
                    "sample_index": index,
                    "global_window_id": index,
                    "url": f"https://example.test/{index}.npy",
                    "source": "source",
                    "manifest_index": 0,
                    "byte_start": index * 2048,
                    "byte_end": (index + 1) * 2048,
                }
                for index in range(2)
            ]
            samples_path = directory / "samples.jsonl"
            samples_path.write_text(
                "".join(json.dumps(record) + "\n" for record in records),
                encoding="utf-8",
            )
            config = download.CohortConfig(
                name="test",
                samples_path=samples_path,
                expected_count=2,
                tokens_path=directory / "tokens.npy",
                summary_path=directory / "summary.json",
            )
            calls: list[int] = []

            def interrupted_fetcher(
                url: str, byte_start: int, byte_end: int, *, timeout: float
            ) -> bytes:
                row = byte_start // 2048
                calls.append(row)
                if row == 1:
                    raise TimeoutError("interrupted")
                return np.full(512, row, dtype="<u4").tobytes()

            with self.assertRaises(TimeoutError):
                download.download_cohort(
                    config,
                    max_workers=1,
                    retries=1,
                    progress_interval=1,
                    range_fetcher=interrupted_fetcher,
                )

            resumed_calls: list[int] = []

            def resumed_fetcher(
                url: str, byte_start: int, byte_end: int, *, timeout: float
            ) -> bytes:
                row = byte_start // 2048
                resumed_calls.append(row)
                return np.full(512, row, dtype="<u4").tobytes()

            summary = download.download_cohort(
                config,
                max_workers=1,
                retries=1,
                progress_interval=1,
                range_fetcher=resumed_fetcher,
            )

            self.assertEqual(calls, [0, 1])
            self.assertEqual(resumed_calls, [1])
            self.assertTrue(summary["resumed"])

    def test_load_cohort_records_rejects_mixed_cohort(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            samples_path = directory / "samples.jsonl"
            samples_path.write_text(
                json.dumps(
                    {
                        "cohort": "ranking",
                        "sample_index": 0,
                        "global_window_id": 1,
                        "url": "https://example.test/shard.npy",
                        "source": "source",
                        "manifest_index": 0,
                        "byte_start": 0,
                        "byte_end": 2048,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            config = download.CohortConfig(
                name="hessian",
                samples_path=samples_path,
                expected_count=1,
                tokens_path=directory / "tokens.npy",
                summary_path=directory / "summary.json",
            )
            with self.assertRaisesRegex(ValueError, "not 'hessian'"):
                download.load_cohort_records(config)


if __name__ == "__main__":
    unittest.main()
