import numpy as np

from product_states import ProductStateMatrix

from math_helper import LANDE_FACTOR, MU_B
from spin import Spin
from spin_expectation_value import calculate_spin_expectation_value


def calculate_magnetization(
    spins: list[Spin],
    eigenvalue_index: int,
    eigenvectors: np.ndarray,
    product_state_matrix: ProductStateMatrix,
) -> complex:
    """
    Calculate the magnetization of a spin system.
    The magnetization is defined as the sum over g * mu_B * e_B * s_i
    where g is the Landé factor, mu_B the Bohr magneton, e_B the unit vector in the direction of the magnetic field.
    """

    result = 0j

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
) -> complex:
    """
    Calculate the magnetization of a spin system.
    The magnetization is defined as the sum over g * mu_B * e_B * s_i
    where g is the Landé factor, mu_B the Bohr magneton, e_B the unit vector in the direction of the magnetic field.
    Uses the spin_expectation_values array instead of recalculating it from scratch.
    """

    result = 0j

    for spin_index, spin in enumerate(spins):
        magnetic_field_direction = spin.B / np.linalg.norm(spin.B)
        spin_expectation_value = spin_expectation_values[eigenvalue_index, spin_index]
        result += LANDE_FACTOR * MU_B * np.dot(magnetic_field_direction, spin_expectation_value)

    return result
