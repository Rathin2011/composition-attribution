"""Unit tests for the J-Lens activation intervention primitives."""

from __future__ import annotations

import unittest

import torch

from jlens_experiments.interventions import (
    LayerIntervention,
    ablate_direction,
    intervene_on_token_positions,
    jlens_token_direction,
    steer_along_direction,
    swap_direction_coordinates,
)


class JLensDirectionTests(unittest.TestCase):
    def test_direction_reproduces_linearized_target_score(self) -> None:
        jacobian = torch.tensor([[2.0, 1.0], [-1.0, 3.0]])
        unembedding_row = torch.tensor([0.5, -2.0])
        delta = torch.tensor([1.5, -0.75])

        direction = jlens_token_direction(jacobian, unembedding_row)

        layer_space_score = torch.dot(direction, delta)
        final_space_score = torch.dot(unembedding_row, jacobian @ delta)
        torch.testing.assert_close(layer_space_score, final_space_score)

    def test_direction_rejects_incompatible_width(self) -> None:
        with self.assertRaisesRegex(ValueError, "unembedding_row"):
            jlens_token_direction(torch.eye(3), torch.ones(2))


class SteeringTests(unittest.TestCase):
    def test_steering_adds_the_requested_vector(self) -> None:
        activation = torch.tensor([1.0, 2.0, 3.0])
        direction = torch.tensor([2.0, 0.0, -1.0])

        edited = steer_along_direction(
            activation,
            direction,
            coefficient=0.5,
        )

        torch.testing.assert_close(edited, torch.tensor([2.0, 2.0, 2.5]))
        torch.testing.assert_close(activation, torch.tensor([1.0, 2.0, 3.0]))

    def test_steering_broadcasts_over_token_rows(self) -> None:
        activations = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
        direction = torch.tensor([2.0, -1.0])

        edited = steer_along_direction(
            activations,
            direction,
            coefficient=-0.25,
        )

        expected = torch.tensor([[0.5, 0.25], [-0.5, 1.25]])
        torch.testing.assert_close(edited, expected)


class AblationTests(unittest.TestCase):
    def test_full_ablation_removes_only_parallel_component(self) -> None:
        activation = torch.tensor([3.0, 4.0])
        direction = torch.tensor([2.0, 0.0])

        edited = ablate_direction(activation, direction)

        torch.testing.assert_close(edited, torch.tensor([0.0, 4.0]))
        torch.testing.assert_close(torch.dot(edited, direction), torch.tensor(0.0))

    def test_partial_ablation_removes_requested_fraction(self) -> None:
        activation = torch.tensor([3.0, 4.0])
        direction = torch.tensor([1.0, 0.0])

        edited = ablate_direction(activation, direction, strength=0.25)

        torch.testing.assert_close(edited, torch.tensor([2.25, 4.0]))

    def test_matrix_ablation_matches_independent_rows(self) -> None:
        activations = torch.tensor([[3.0, 4.0], [5.0, 12.0]])
        direction = torch.tensor([1.0, 0.0])

        edited = ablate_direction(activations, direction)

        torch.testing.assert_close(
            edited,
            torch.tensor([[0.0, 4.0], [0.0, 12.0]]),
        )

    def test_ablation_preserves_activation_dtype(self) -> None:
        activation = torch.tensor([3.0, 4.0], dtype=torch.bfloat16)
        direction = torch.tensor([1.0, 0.0])

        edited = ablate_direction(activation, direction)

        self.assertEqual(edited.dtype, torch.bfloat16)
        torch.testing.assert_close(edited.float(), torch.tensor([0.0, 4.0]))

    def test_invalid_strength_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "strength"):
            ablate_direction(
                torch.ones(3),
                torch.ones(3),
                strength=1.1,
            )


class CoordinateSwapTests(unittest.TestCase):
    def test_full_swap_exchanges_coordinates_and_preserves_remainder(self) -> None:
        activation = torch.tensor([3.0, 1.0, 5.0])
        source = torch.tensor([1.0, 0.0, 0.0])
        target = torch.tensor([0.0, 1.0, 0.0])

        edited = swap_direction_coordinates(activation, source, target)

        torch.testing.assert_close(edited, torch.tensor([1.0, 3.0, 5.0]))

    def test_scaled_swap_interpolates_toward_exchanged_coordinates(self) -> None:
        activation = torch.tensor([3.0, 1.0, 5.0])

        edited = swap_direction_coordinates(
            activation,
            torch.tensor([1.0, 0.0, 0.0]),
            torch.tensor([0.0, 1.0, 0.0]),
            scale=0.5,
        )

        torch.testing.assert_close(edited, torch.tensor([2.0, 2.0, 5.0]))

    def test_collinear_directions_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "linearly independent"):
            swap_direction_coordinates(
                torch.ones(2),
                torch.tensor([1.0, 0.0]),
                torch.tensor([2.0, 0.0]),
            )


class TokenPositionInterventionTests(unittest.TestCase):
    def test_steering_changes_only_selected_token_rows(self) -> None:
        hidden_states = torch.zeros(1, 3, 2)
        direction = torch.tensor([1.0, -2.0])

        edited = intervene_on_token_positions(
            hidden_states,
            direction,
            token_positions=(0, 2),
            kind="steer",
            coefficient=0.5,
        )

        expected = torch.tensor([[[0.5, -1.0], [0.0, 0.0], [0.5, -1.0]]])
        torch.testing.assert_close(edited, expected)
        torch.testing.assert_close(hidden_states, torch.zeros_like(hidden_states))

    def test_none_selects_every_token_position(self) -> None:
        hidden_states = torch.tensor([[[3.0, 4.0], [5.0, 6.0]]])

        edited = intervene_on_token_positions(
            hidden_states,
            torch.tensor([1.0, 0.0]),
            token_positions=None,
            kind="ablate",
        )

        torch.testing.assert_close(
            edited,
            torch.tensor([[[0.0, 4.0], [0.0, 6.0]]]),
        )

    def test_negative_position_selects_final_token(self) -> None:
        hidden_states = torch.zeros(1, 2, 2)

        edited = intervene_on_token_positions(
            hidden_states,
            torch.tensor([1.0, 0.0]),
            token_positions=(-1,),
            kind="steer",
            coefficient=2.0,
        )

        torch.testing.assert_close(
            edited,
            torch.tensor([[[0.0, 0.0], [2.0, 0.0]]]),
        )

    def test_swap_changes_only_selected_token_row(self) -> None:
        hidden_states = torch.tensor([[[3.0, 1.0], [5.0, 2.0]]])

        edited = intervene_on_token_positions(
            hidden_states,
            torch.tensor([1.0, 0.0]),
            target_direction=torch.tensor([0.0, 1.0]),
            token_positions=(1,),
            kind="swap",
        )

        torch.testing.assert_close(
            edited,
            torch.tensor([[[3.0, 1.0], [2.0, 5.0]]]),
        )


class LayerInterventionTests(unittest.TestCase):
    def test_hook_edits_tensor_output_and_is_removed_after_context(self) -> None:
        block = torch.nn.Identity()
        hidden_states = torch.zeros(1, 2, 2)
        intervention = LayerIntervention(
            [block],
            layer_index=0,
            token_positions=(1,),
            direction=torch.tensor([1.0, 0.0]),
            kind="steer",
            coefficient=3.0,
        )

        with intervention:
            edited = block(hidden_states)
        unedited = block(hidden_states)

        torch.testing.assert_close(
            edited,
            torch.tensor([[[0.0, 0.0], [3.0, 0.0]]]),
        )
        torch.testing.assert_close(unedited, hidden_states)

    def test_hook_preserves_tuple_metadata(self) -> None:
        class TupleBlock(torch.nn.Module):
            def forward(self, hidden_states: torch.Tensor):
                return hidden_states, "cache"

        block = TupleBlock()
        hidden_states = torch.tensor([[[3.0, 4.0]]])
        intervention = LayerIntervention(
            [block],
            layer_index=0,
            token_positions=None,
            direction=torch.tensor([1.0, 0.0]),
            kind="ablate",
        )

        with intervention:
            output = block(hidden_states)

        torch.testing.assert_close(output[0], torch.tensor([[[0.0, 4.0]]]))
        self.assertEqual(output[1], "cache")

    def test_invalid_layer_is_rejected_before_forward(self) -> None:
        with self.assertRaisesRegex(IndexError, "layer_index"):
            LayerIntervention(
                [torch.nn.Identity()],
                layer_index=1,
                token_positions=None,
                direction=torch.ones(2),
                kind="ablate",
            )

    def test_hook_supports_coordinate_swap(self) -> None:
        block = torch.nn.Identity()
        hidden_states = torch.tensor([[[4.0, 1.0]]])
        intervention = LayerIntervention(
            [block],
            layer_index=0,
            token_positions=(-1,),
            direction=torch.tensor([1.0, 0.0]),
            target_direction=torch.tensor([0.0, 1.0]),
            kind="swap",
        )

        with intervention:
            edited = block(hidden_states)

        torch.testing.assert_close(edited, torch.tensor([[[1.0, 4.0]]]))


if __name__ == "__main__":
    unittest.main()
