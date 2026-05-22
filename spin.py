from enum import Enum, auto

import numpy as np

from math_helper import PI, get_rotation_matrix_around_z_axis, number


class Spin:

    def __init__(self,
            spin: number,
            position: np.ndarray,
            anisotropy_value: number,
            anisotropy_axis: np.ndarray,
            magnetic_field: np.ndarray
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
    """Represents a C_N-rotationally symmetric group of spins around z-axis"""

    class MagneticFieldType(Enum):
        linear = auto()
        circular = auto()
    

    small_x = np.array([0.00000001, 0, 0])
    zero = np.array([0, 0, 0])


    def __init__(
            self, 
            number_of_spins: int, 
            spin: number,
            heisenberg_interaction_constant: number,
            first_position: np.ndarray = zero, 
            first_magnetic_field: np.ndarray = zero,
            magnetic_field_type: MagneticFieldType = MagneticFieldType.linear,  
            first_anisotropy_axis: np.ndarray = zero,
            anisotropy_value: number = 0,
    ):
        self._rotation_matrices: list[np.ndarray] = [
            get_rotation_matrix_around_z_axis(2 * PI * i / number_of_spins) for i in range(number_of_spins)
        ]
        self.number_of_spins = number_of_spins
        self.spin = spin
        self.heisenberg_interaction_constant = heisenberg_interaction_constant
        self.heisenberg_interaction_matrix = self.get_heisenberg_interaction_matrix()
        self.first_position = first_position
        self.first_magnetic_field = first_magnetic_field
        self.magnetic_field_type = magnetic_field_type
        self.first_anisotropy_axis = first_anisotropy_axis
        self.anisotropy_value = anisotropy_value

        self.spins: list[Spin] = [Spin(
            spin=spin,
            position=self._rotate_to_nth_position(self.first_position, n),
            magnetic_field=self._get_magnetic_field_for_nth_spin(n),
            anisotropy_axis=self._rotate_to_nth_position(self.first_anisotropy_axis, n),
            anisotropy_value=self.anisotropy_value
        ) for n in range(number_of_spins)]


    def set_magnetic_field_for_all(
            self, 
            first_magnetic_field: np.ndarray, 
            magnetic_field_type: MagneticFieldType = MagneticFieldType.linear
    ) -> SpinRing:
        self.first_magnetic_field = first_magnetic_field
        self.magnetic_field_type = magnetic_field_type
        for n in range(self.number_of_spins):
            self.spins[n].magnetic_field = self._get_magnetic_field_for_nth_spin(n)
        return self

    def _get_magnetic_field_for_nth_spin(self, n: int):
        if self.magnetic_field_type == self.MagneticFieldType.linear:
            return self.first_magnetic_field
        magnetic_field = self._rotate_to_nth_position(self.first_magnetic_field, n)
        magnetic_field = self._break_degeneracy(magnetic_field) # TODO maybe add a toggle?
        return magnetic_field

    def _break_degeneracy(self, magnetic_field: np.ndarray) -> np.ndarray:
        return magnetic_field + self.small_x   
        

    def set_anisotropy_axes_for_all(self, first_anisotropy_axis: np.ndarray) -> SpinRing:        
        self.first_anisotropy_axis = first_anisotropy_axis
        for n in range(self.number_of_spins):
            self.spins[n].anisotropy_axis = self._rotate_to_nth_position(self.first_anisotropy_axis, n)
        return self


    def _rotate_to_nth_position(self, vector: np.ndarray, n: int) -> np.ndarray:
        return np.dot(self._rotation_matrices[n], vector)
    

    def get_heisenberg_interaction_matrix(self) -> np.ndarray:
        matrix = np.zeros([self.number_of_spins, self.number_of_spins])
        for i in range(self.number_of_spins - 1):
            matrix[i+1, i] = self.heisenberg_interaction_constant
        matrix[self.number_of_spins - 1, 0] = self.heisenberg_interaction_constant
        return matrix
