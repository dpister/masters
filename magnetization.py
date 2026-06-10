import numpy as np

from product_states import ProductStateMatrix

from math_helper import LANDE_FACTOR, MU_B, number
from spin import Spin
from spin_expectation_value import calculate_spin_expectation_value


def calculate_magnetization(
    spins: list[Spin],
    eigenvalue_index: int,
    eigenvectors: np.ndarray,
    product_state_matrix: ProductStateMatrix,
) -> number:

    result = 0

    for spin_index, spin in enumerate(spins):
        magnetic_field_direction = spin.B / np.linalg.norm(spin.B)
        spin_expectation_value = calculate_spin_expectation_value(
            spin_index=spin_index,
            product_state_matrix=product_state_matrix,
            eigenvectors=eigenvectors,
            eigenvalue_index=eigenvalue_index,
        )
        result += LANDE_FACTOR * MU_B * np.dot(magnetic_field_direction, spin_expectation_value)

    return result


def calculate_magnetization_from_spin_expectation_values(
    spins: list[Spin],
    eigenvalue_index: int,
    spin_expectation_values: np.ndarray,
) -> number:

    result = 0

    for spin_index, spin in enumerate(spins):
        magnetic_field_direction = spin.B / np.linalg.norm(spin.B)
        spin_expectation_value = spin_expectation_values[eigenvalue_index, spin_index]
        result += LANDE_FACTOR * MU_B * np.dot(magnetic_field_direction, spin_expectation_value)

    return result
