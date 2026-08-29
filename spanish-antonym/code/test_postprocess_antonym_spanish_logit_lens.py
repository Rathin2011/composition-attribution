import unittest

from postprocess_antonym_spanish_logit_lens import build_summary, partition_records


def record(index: int, intermediate: str, group: str) -> dict:
    return {
        "evaluation_index": index,
        "classification": {
            "selected_intermediate": intermediate,
            "group": group,
        },
    }


class PostprocessAntonymSpanishLogitLensTest(unittest.TestCase):
    def test_partitions_groups_and_compositional_paths(self) -> None:
        fx = [record(1, "Fx", "compositional"), record(2, "Fx", "ambiguous")]
        gx = [
            record(3, "Gx", "compositional"),
            record(4, "Gx", "shortcut_candidate"),
        ]

        compositional, ambiguous, shortcut, compositional_fx, compositional_gx = (
            partition_records(fx, gx)
        )

        self.assertEqual([item["evaluation_index"] for item in compositional], [1, 3])
        self.assertEqual([item["evaluation_index"] for item in ambiguous], [2])
        self.assertEqual([item["evaluation_index"] for item in shortcut], [4])
        self.assertEqual([item["evaluation_index"] for item in compositional_fx], [1])
        self.assertEqual([item["evaluation_index"] for item in compositional_gx], [3])

    def test_summary_reports_groups_and_paths(self) -> None:
        compositional = [record(1, "Fx", "compositional"), record(2, "Gx", "compositional")]
        summary = build_summary(
            compositional,
            [record(3, "Fx", "ambiguous")],
            [record(4, "Gx", "shortcut_candidate")],
            [compositional[0]],
            [compositional[1]],
            raw_correct=5,
            paper_token_eligible=4,
        )

        self.assertEqual(summary["paper_token_excluded"], 1)
        self.assertEqual(summary["num_compositional"], 2)
        self.assertEqual(summary["num_ambiguous"], 1)
        self.assertEqual(summary["num_shortcut_candidates"], 1)
        self.assertEqual(summary["num_compositional_antonym_then_translate"], 1)
        self.assertEqual(summary["num_compositional_translate_then_antonym"], 1)
        self.assertEqual(summary["p_compositional_given_correct_eligible"], 0.5)

    def test_rejects_path_file_with_wrong_intermediate(self) -> None:
        with self.assertRaises(ValueError):
            partition_records([record(1, "Gx", "compositional")], [])


if __name__ == "__main__":
    unittest.main()
