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


if __name__ == "__main__":
    unittest.main()
