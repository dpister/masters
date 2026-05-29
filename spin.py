from __future__ import annotations
from enum import Enum

import numpy as np

from math_helper import (
    PI,
    get_rotation_matrix_around_z_axis,
    get_x_unit_vector_tilted_in_xy_plane,
    number,
    e_y,
)


class Spin:
    def __init__(
        self,
        spin: number,
        position: np.ndarray,
        anisotropy_value: number,
        anisotropy_axis: np.ndarray,
        magnetic_field: np.ndarray,
    ):
        self.spin = spin
        self.position = position
        self.anisotropy_value = anisotropy_value
        self.anisotropy_axis = anisotropy_axis
        self.magnetic_field = magnetic_field

    @property
    def s(self) -> number:
        return self.spin

    @property
    def D(self) -> number:
        return self.anisotropy_value

    @property
    def D_x(self) -> number:
        return self.anisotropy_axis[0]

    @property
    def D_y(self) -> number:
        return self.anisotropy_axis[1]

    @property
    def D_z(self) -> number:
        return self.anisotropy_axis[2]

    @property
    def B_x(self) -> number:
        return self.magnetic_field[0]

    @property
    def B_y(self) -> number:
        return self.magnetic_field[1]

    @property
    def B_z(self) -> number:
        return self.magnetic_field[2]

    @property
    def r_x(self) -> number:
        return self.position[0]

    @property
    def r_y(self) -> number:
        return self.position[1]

    @property
    def r_z(self) -> number:
        return self.position[2]


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

    small_x = np.array([0.00000001, 0, 0])
    zero = np.array([0, 0, 0])

    def __init__(
        self,
        number_of_spins: int,
        spin: number,
        heisenberg_interaction_constant: number,
        magnetic_field_of_first_spin: np.ndarray = zero,
        magnetic_field_type: str = MagneticFieldType.linear.value,
        anisotropy_axis_angle: number = 0,
        anisotropy_value: number = 0,
    ):
        self._rotation_matrices: list[np.ndarray] = [
            get_rotation_matrix_around_z_axis(2 * PI * i / number_of_spins)
            for i in range(number_of_spins)
        ]
        self.number_of_spins = number_of_spins
        self.spin = spin
        self.heisenberg_interaction_constant = heisenberg_interaction_constant
        self.heisenberg_interaction_matrix = self.get_heisenberg_interaction_matrix(
            heisenberg_interaction_constant
        )
        self.magnetic_field_of_first_spin = magnetic_field_of_first_spin
        self.magnetic_field_type = magnetic_field_type

        self.position_of_first_spin = e_y
        self.anisotropy_axes_angle = anisotropy_axis_angle
        self.anisotropy_axis_of_first_spin = get_x_unit_vector_tilted_in_xy_plane(
            anisotropy_axis_angle
        )
        self.anisotropy_value = anisotropy_value

        self.spins: list[Spin] = [
            Spin(
                spin=spin,
                position=self._rotate_to_nth_position(self.position_of_first_spin, n),
                magnetic_field=self._get_magnetic_field_for_nth_spin(n),
                anisotropy_axis=self._rotate_to_nth_position(self.anisotropy_axis_of_first_spin, n),
                anisotropy_value=self.anisotropy_value,
            )
            for n in range(number_of_spins)
        ]

    def set_magnetic_field_for_all(
        self,
        magnetic_field_of_first_spin: np.ndarray,
        magnetic_field_type: str = MagneticFieldType.linear.value,
    ) -> SpinRing:
        self.magnetic_field_of_first_spin = magnetic_field_of_first_spin
        self.magnetic_field_type = magnetic_field_type
        for n in range(self.number_of_spins):
            self.spins[n].magnetic_field = self._get_magnetic_field_for_nth_spin(n)
        return self

    def _get_magnetic_field_for_nth_spin(self, n: int):
        if self.magnetic_field_type == self.MagneticFieldType.linear:
            return self.magnetic_field_of_first_spin
        magnetic_field = self._rotate_to_nth_position(self.magnetic_field_of_first_spin, n)
        magnetic_field = self._break_degeneracy(magnetic_field)  # TODO maybe add a toggle?
        return magnetic_field

    def _break_degeneracy(self, magnetic_field: np.ndarray) -> np.ndarray:
        return magnetic_field + self.small_x

    def set_anisotropy_axes_for_all(self, angle_degrees: number) -> SpinRing:
        self.anisotropy_axis_of_first_spin = get_x_unit_vector_tilted_in_xy_plane(angle_degrees)
        for n in range(self.number_of_spins):
            self.spins[n].anisotropy_axis = self._rotate_to_nth_position(
                self.anisotropy_axis_of_first_spin, n
            )
        return self

    def _rotate_to_nth_position(self, vector: np.ndarray, n: int) -> np.ndarray:
        return np.dot(self._rotation_matrices[n], vector)

    def get_heisenberg_interaction_matrix(
        self, heisenberg_interaction_constant: number
    ) -> np.ndarray:
        matrix = np.zeros([self.number_of_spins, self.number_of_spins])
        for i in range(self.number_of_spins - 1):
            matrix[i + 1, i] = heisenberg_interaction_constant
        matrix[self.number_of_spins - 1, 0] = heisenberg_interaction_constant
        return matrix
