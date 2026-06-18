import numpy as np

from product_states import ProductStateMatrix
from spin import Spin
from spin_expectation_value import calculate_spin_expectation_value


def calculate_toroidal_moment(
    spins: list[Spin], eigenvalue_index: int, eigenvectors: np.ndarray, product_state_matrix: ProductStateMatrix
) -> np.ndarray:

    result = np.zeros(3, dtype=np.complex128)

    for spin_index, spin in enumerate(spins):
        spin_expectation_value = calculate_spin_expectation_value(
            spin_index=spin_index,
            eigenvalue_index=eigenvalue_index,
            product_state_matrix=product_state_matrix,
            eigenvectors=eigenvectors,
        )

        result += np.cross(spin.position, spin_expectation_value)

    return result


def calculate_toroidal_moment_from_spin_expectation_values(
    spins: list[Spin], spin_expectation_values: np.ndarray, eigenvalue_index: int
) -> np.ndarray:

    result = np.zeros(3, dtype=np.complex128)

    for spin_index, spin in enumerate(spins):
        spin_expectation_value = spin_expectation_values[eigenvalue_index, spin_index]
        result += np.cross(spin.position, spin_expectation_value)

    return result
