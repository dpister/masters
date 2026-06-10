import math

import numpy as np

from product_states import ProductStateMatrix
from spin import Spin


def calculate_single_spin_alignment(
    spin_index: int,
    spin: Spin,
    eigenvalue_index: int,
    product_state_matrix: ProductStateMatrix,
    eigenvectors: np.ndarray,
) -> complex:
    """"""

    number_of_states = product_state_matrix.number_of_product_states

    result = 0j

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            m = product_state_matrix.spin(spin_index)[j]
            s = product_state_matrix.spin_values[spin_index]
            c_i: complex = eigenvectors[i, eigenvalue_index]
            c_j: complex = eigenvectors[j, eigenvalue_index]

            if i == j:
                result += spin.D * c_i.conjugate() * c_j * (spin.e_D_z * m) ** 2
                result += (
                    spin.D
                    * c_i.conjugate()
                    * c_j
                    * (2 * s * (s + 1) - 2 * m**2)
                    * (1 / 4 * spin.e_D_x**2 + 1 / 4 * spin.e_D_y**2)
                )

            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, +1):
                result += (
                    spin.D
                    * c_i.conjugate()
                    * c_j
                    * math.sqrt(s * (s + 1) - m * (m + 1))
                    * (2 * m + 1)
                    * (1 / 2 * spin.e_D_x * spin.e_D_z - 1j / 2 * spin.e_D_y * spin.e_D_z)
                )

            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, -1):
                result += (
                    spin.D
                    * c_i.conjugate()
                    * c_j
                    * math.sqrt(s * (s + 1) - m * (m - 1))
                    * (2 * m - 1)
                    * (1 / 2 * spin.e_D_x * spin.e_D_z + 1j / 2 * spin.e_D_y * spin.e_D_z)
                )

            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, +2):
                result += (
                    spin.D
                    * c_i.conjugate()
                    * c_j
                    * math.sqrt(s * (s + 1) - m * (m + 1))
                    * math.sqrt(s * (s + 1) - (m + 1) * (m + 2))
                    * (1 / 4 * spin.e_D_x**2 - 1 / 4 * spin.e_D_y**2 - 1j / 2 * spin.e_D_x * spin.e_D_y)
                )

            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, -2):
                result += (
                    spin.D
                    * c_i.conjugate()
                    * c_j
                    * math.sqrt(s * (s + 1) - m * (m - 1))
                    * math.sqrt(s * (s + 1) - (m - 1) * (m - 2))
                    * (1 / 4 * spin.e_D_x**2 - 1 / 4 * spin.e_D_y**2 + 1j / 2 * spin.e_D_x * spin.e_D_y)
                )

    return result


def calculate_alignment(
    spins: list[Spin],
    eigenvalue_index: int,
    product_state_matrix: ProductStateMatrix,
    eigenvectors: np.ndarray,
) -> complex:

    result = 0j

    for spin_index, spin in enumerate(spins):
        result += calculate_single_spin_alignment(
            spin=spin,
            spin_index=spin_index,
            eigenvalue_index=eigenvalue_index,
            product_state_matrix=product_state_matrix,
            eigenvectors=eigenvectors,
        )

    return result
