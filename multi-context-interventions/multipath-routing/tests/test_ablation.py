import sys
from pathlib import Path
import unittest

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from multipath.ablation import (ablate, matched_random_tokens, orthonormal_basis,
    projection_fraction)


class AblationTest(unittest.TestCase):
    def test_basis_drops_dependent_rows(self):
        rows = torch.tensor([[1.0, 0, 0], [2.0, 0, 0], [0, 1.0, 0]])
        q = orthonormal_basis(rows)
        self.assertEqual(q.shape, (3, 2))
        self.assertTrue(torch.allclose(q.T @ q, torch.eye(2), atol=1e-6))

    def test_zero_ablation_removes_component(self):
        q = orthonormal_basis(torch.tensor([[1.0, 1.0, 0]]))
        out = ablate(torch.tensor([3.0, 1.0, 5.0]), q, None)
        self.assertAlmostEqual(float((q.T @ out).abs().max()), 0.0, places=5)
        self.assertAlmostEqual(float(out[2]), 5.0, places=5)

    def test_mean_ablation_sets_component_to_mean(self):
        q = orthonormal_basis(torch.tensor([[0, 1.0, 0]]))
        mean = torch.tensor([9.0, 7.0, 9.0])
        out = ablate(torch.tensor([1.0, 2.0, 3.0]), q, mean)
        self.assertTrue(torch.allclose(out, torch.tensor([1.0, 7.0, 3.0])))

    def test_projection_fraction(self):
        q = orthonormal_basis(torch.tensor([[1.0, 0, 0]]))
        self.assertAlmostEqual(projection_fraction(torch.tensor([1.0, 1.0, 0]), q), 2 ** -0.5, places=5)

    def test_matched_random_is_deterministic_and_excludes(self):
        mask = torch.ones(100, dtype=torch.bool)
        a = matched_random_tokens([10, 50], mask, excluded={10, 50}, window=5, seed_key="p:0")
        b = matched_random_tokens([10, 50], mask, excluded={10, 50}, window=5, seed_key="p:0")
        self.assertEqual(a, b)
        self.assertTrue(all(abs(x - r) <= 5 and x not in {10, 50} for x, r in zip(a, [10, 50])))


if __name__ == "__main__":
    unittest.main()
