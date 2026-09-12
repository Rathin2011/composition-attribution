from pathlib import Path
import tempfile
import unittest

import stage1_data as stream


class StageOneDataTest(unittest.TestCase):
    def test_recipe_constants_are_consistent(self) -> None:
        stream.validate_recipe()
        self.assertEqual(stream.TRAIN_SEQUENCE_LENGTH, 8_192)
        self.assertEqual(stream.ANALYSIS_WINDOW_LENGTH, 512)
        self.assertEqual(stream.WINDOWS_PER_TRAIN_SEQUENCE, 16)
        self.assertEqual(stream.GLOBAL_BATCH_SEQUENCES, 512)
        self.assertEqual(stream.STAGE_ONE_SHUFFLE_SEED, 34_522)
        self.assertEqual(stream.STAGE_ONE_INSTANCES_SEEN, 723_872_768)

    def test_parse_manifest_resolves_official_tokenizer(self) -> None:
        text = (
            "# comment\n"
            "common_crawl,preprocessed/{TOKENIZER}/common_crawl/000000.npy\n"
            "papers,preprocessed/{TOKENIZER}/papers/000001.npy\n"
        )

        entries = stream.parse_manifest_text(text)

        self.assertEqual(
            [entry.source for entry in entries], ["common_crawl", "papers"]
        )
        self.assertEqual(
            entries[0].relative_path,
            "preprocessed/allenai/dolma3-tokenizer/common_crawl/000000.npy",
        )
        self.assertEqual(
            entries[0].url,
            "https://olmo-data.org/preprocessed/allenai/dolma3-tokenizer/"
            "common_crawl/000000.npy",
        )

    def test_parse_manifest_rejects_ambiguous_input(self) -> None:
        invalid_manifests = [
            "source,path,extra\n",
            "source,missing-placeholder.npy\n",
            "source,{TOKENIZER}/not-numpy.bin\n",
            "source,/{TOKENIZER}/absolute.npy\n",
            "source,{TOKENIZER}/same.npy\nsource,{TOKENIZER}/same.npy\n",
        ]
        for text in invalid_manifests:
            with self.subTest(text=text), self.assertRaises(ValueError):
                stream.parse_manifest_text(text)

    def test_load_official_manifest_rejects_modified_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = Path(temp_dir) / stream.MANIFEST_FILENAME
            manifest.write_bytes(b"source,path.npy\n")

            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                stream.load_official_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
