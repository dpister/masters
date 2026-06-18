import math

import numpy as np

from product_states import ProductStateMatrix


def calculate_spin_expectation_value(
    spin_index: int, eigenvalue_index: int, product_state_matrix: ProductStateMatrix, eigenvectors: np.ndarray
) -> np.ndarray:

    number_of_states = product_state_matrix.number_of_product_states

    result = np.zeros(3, dtype=np.complex128)

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            m = product_state_matrix.spin(spin_index)[j]
            s = product_state_matrix.spin_values[spin_index]
            c_i: complex = eigenvectors[i, eigenvalue_index]
            c_j: complex = eigenvectors[j, eigenvalue_index]

            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, +1):
                result[0] += 1 / 2 * c_i.conjugate() * c_j * math.sqrt(s * (s + 1) - m * (m + 1))
                result[1] += -1j / 2 * c_i.conjugate() * c_j * math.sqrt(s * (s + 1) - m * (m + 1))
            #
            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, -1):
                result[0] += 1 / 2 * c_i.conjugate() * c_j * math.sqrt(s * (s + 1) - m * (m - 1))
                result[1] += 1j / 2 * c_i.conjugate() * c_j * math.sqrt(s * (s + 1) - m * (m - 1))

            if i == j:
                result[2] += m * c_i.conjugate() * c_j

    return result
