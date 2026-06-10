from __future__ import annotations
import numpy as np

from math_helper import number


class Spin:
    """"""

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
    def e_D_x(self) -> number:
        return self.anisotropy_axis[0]

    @property
    def e_D_y(self) -> number:
        return self.anisotropy_axis[1]

    @property
    def e_D_z(self) -> number:
        return self.anisotropy_axis[2]

    @property
    def e_D(self) -> np.ndarray:
        return self.anisotropy_axis

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
    def B(self) -> np.ndarray:
        return self.magnetic_field

    @property
    def r_x(self) -> number:
        return self.position[0]

    @property
    def r_y(self) -> number:
        return self.position[1]

    @property
    def r_z(self) -> number:
        return self.position[2]

    @property
    def r(self) -> np.ndarray:
        return self.position
