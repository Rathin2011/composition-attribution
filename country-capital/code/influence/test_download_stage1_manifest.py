from hashlib import sha256
from pathlib import Path
import tempfile
import unittest

import download_stage1_manifest as download


FIXTURE = b"source_a,path/{TOKENIZER}/000000.npy\n"
FIXTURE_SHA256 = sha256(FIXTURE).hexdigest()


class DownloadStageOneManifestTest(unittest.TestCase):
    def test_verify_manifest_bytes_accepts_valid_content(self) -> None:
        count = download.verify_manifest_bytes(
            FIXTURE,
            expected_sha256=FIXTURE_SHA256,
            expected_shard_count=1,
        )
        self.assertEqual(count, 1)

    def test_verify_manifest_bytes_rejects_wrong_hash(self) -> None:
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            download.verify_manifest_bytes(
                FIXTURE,
                expected_sha256="0" * 64,
                expected_shard_count=1,
            )

    def test_verify_manifest_bytes_rejects_wrong_shard_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "shard-count mismatch"):
            download.verify_manifest_bytes(
                FIXTURE,
                expected_sha256=FIXTURE_SHA256,
                expected_shard_count=2,
            )

    def test_download_manifest_saves_exact_verified_bytes(self) -> None:
        def fake_fetcher(url: str, timeout: float) -> bytes:
            self.assertEqual(url, download.MANIFEST_URL)
            self.assertEqual(timeout, 12.0)
            return FIXTURE

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifest.txt"
            saved_path = download.download_manifest(
                output,
                timeout=12.0,
                verbose=False,
                fetcher=fake_fetcher,
                expected_sha256=FIXTURE_SHA256,
                expected_shard_count=1,
            )

            self.assertEqual(saved_path, output)
            self.assertEqual(output.read_bytes(), FIXTURE)
            self.assertFalse((output.parent / ".manifest.txt.tmp").exists())


if __name__ == "__main__":
    unittest.main()
