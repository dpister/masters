from __future__ import annotations
from copy import deepcopy
from enum import Enum

import numpy as np
from math_helper import PI, get_rotation_matrix_around_z_axis, get_x_unit_vector_tilted_in_xy_plane, number, e_y, e_z
from product_states import ProductStateMatrix
from spin import Spin


class SpinRing:
    """
    Represents a group of spins that is C_N-rotationally symmetrical around z-axis.
    The hamiltonian is invariant under collective rotation of anisotropy axes around the z-axis.
    So we place the spins on a unit circle of arbitrary units
    and choose the anisotropy axes to be tangential
    """

    class MagneticFieldType(Enum):
        linear = "linear"
        circular = "circular"

    ZERO = np.array([0, 0, 0])

    def __init__(
        self,
        number_of_spins: int,
        spin: number,
        heisenberg_interaction_constant: number,
        anisotropy_value: number,
        magnetic_field_direction_of_first_spin: np.ndarray = e_z,
        magnetic_field_type: str = MagneticFieldType.linear.value,
        magnetic_field_strength: number = 0,
        anisotropy_axis_angle: number = 0,
    ):
        self._rotation_matrices: list[np.ndarray] = [
            get_rotation_matrix_around_z_axis(2 * PI * i / number_of_spins) for i in range(number_of_spins)
        ]
        self.number_of_spins = number_of_spins
        self.spin = spin
        self.heisenberg_interaction_constant = heisenberg_interaction_constant
        self.heisenberg_interaction_matrix = self.calculate_heisenberg_interaction_matrix(
            heisenberg_interaction_constant
        )
        self.magnetic_field_direction_of_first_spin = magnetic_field_direction_of_first_spin
        self.magnetic_field_strength = magnetic_field_strength
        self.magnetic_field_type = magnetic_field_type

        self.position_of_first_spin = e_y
        self.anisotropy_axes_angle = anisotropy_axis_angle
        self.anisotropy_axis_of_first_spin = get_x_unit_vector_tilted_in_xy_plane(anisotropy_axis_angle)
        self.anisotropy_value = anisotropy_value

        self.product_state_matrix = ProductStateMatrix(spin_values=[spin] * number_of_spins)

        self.spins: list[Spin] = [
            Spin(
                spin=spin,
                position=self._rotate_to_nth_position(self.position_of_first_spin, n),
                magnetic_field=self._get_magnetic_field_for_nth_spin(n, magnetic_field_strength),
                anisotropy_axis=self._rotate_to_nth_position(self.anisotropy_axis_of_first_spin, n),
                anisotropy_value=self.anisotropy_value,
            )
            for n in range(number_of_spins)
        ]

    def change_magnetic_field_strength(self, magnetic_field_strength: number) -> SpinRing:
        self.magnetic_field_strength = magnetic_field_strength
        for n in range(self.number_of_spins):
            self.spins[n].magnetic_field = self._get_magnetic_field_for_nth_spin(n, magnetic_field_strength)
        return self

    def _get_magnetic_field_for_nth_spin(self, n: int, magnetic_field_strength: number) -> np.ndarray:
        if self.magnetic_field_type == self.MagneticFieldType.linear:
            return self.magnetic_field_direction_of_first_spin * magnetic_field_strength
        magnetic_field_direction = self._rotate_to_nth_position(self.magnetic_field_direction_of_first_spin, n)
        return magnetic_field_direction * magnetic_field_strength + np.array([0.001, 0, 0])

    def change_anisotropy_axes_angle(self, angle_degrees: number) -> SpinRing:
        self.anisotropy_axes_angle = angle_degrees
        self.anisotropy_axis_of_first_spin = get_x_unit_vector_tilted_in_xy_plane(angle_degrees)
        for n in range(self.number_of_spins):
            self.spins[n].anisotropy_axis = self._rotate_to_nth_position(self.anisotropy_axis_of_first_spin, n)
        return self

    def _rotate_to_nth_position(self, vector: np.ndarray, n: int) -> np.ndarray:
        return np.dot(self._rotation_matrices[n], vector)

    def calculate_heisenberg_interaction_matrix(self, heisenberg_interaction_constant: number) -> np.ndarray:
        matrix = np.zeros([self.number_of_spins, self.number_of_spins])
        for i in range(self.number_of_spins - 1):
            matrix[i + 1, i] = heisenberg_interaction_constant
        matrix[self.number_of_spins - 1, 0] = heisenberg_interaction_constant
        return matrix

    def get_copy(self) -> SpinRing:
        return deepcopy(self)
