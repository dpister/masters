import math

import numpy as np

from math_helper import MU_B, LANDE_FACTOR
from product_states import ProductStateMatrix
from spin import Spin


def get_heisenberg_interaction_hamiltonian_matrix(
    heisenberg_interaction_matrix: np.ndarray, product_state_matrix: ProductStateMatrix
) -> np.ndarray:
    """
    Generate the Hamiltonian matrix for the Heisenberg interaction
    """

    assert len(heisenberg_interaction_matrix.shape) == 2
    assert heisenberg_interaction_matrix.shape[0] == heisenberg_interaction_matrix.shape[1]

    J = heisenberg_interaction_matrix
    number_of_spins = product_state_matrix.number_of_spins
    number_of_states = product_state_matrix.number_of_product_states

    hamiltonian = np.zeros([number_of_states, number_of_states]) * 1j

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            for spin1 in range(number_of_spins):
                m1 = product_state_matrix.spin(spin1)[j]
                s1 = product_state_matrix.spin_values[spin1]

                for spin2 in range(spin1):
                    m2 = product_state_matrix.spin(spin2)[j]
                    s2 = product_state_matrix.spin_values[spin2]

                    if i == j:
                        hamiltonian[i, i] += m1 * m2 * J[spin1, spin2]

                    if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin1, +1).changed(
                        spin2, -1
                    ):
                        hamiltonian[i, j] += (
                            J[spin1, spin2]
                            / 2
                            * math.sqrt(s1 * (s1 + 1) - m1 * (m1 + 1))
                            * math.sqrt(s2 * (s2 + 1) - m2 * (m2 - 1))
                        )

                    if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin1, -1).changed(
                        spin2, +1
                    ):
                        hamiltonian[i, j] += (
                            J[spin1, spin2]
                            / 2
                            * math.sqrt(s1 * (s1 + 1) - m1 * (m1 - 1))
                            * math.sqrt(s2 * (s2 + 1) - m2 * (m2 + 1))
                        )

    return hamiltonian


def get_zeeman_hamiltonian_matrix(spins: list[Spin], product_state_matrix: ProductStateMatrix) -> np.ndarray:
    """Generate the Hamiltonian matrix of the Zeeman term using the product basis"""

    number_of_spins = product_state_matrix.number_of_spins
    number_of_states = product_state_matrix.number_of_product_states

    hamiltonian = np.zeros([number_of_states, number_of_states]) * 1j

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            for spin_index in range(number_of_spins):
                spin = spins[spin_index]
                m = product_state_matrix.spin(spin_index)[j]
                s = product_state_matrix.spin_values[spin_index]

                if i == j:
                    hamiltonian[i, j] += LANDE_FACTOR * MU_B * m * spin.B_z

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, +1):
                    hamiltonian[i, j] += (
                        1 / 2 * LANDE_FACTOR * MU_B * math.sqrt(s * (s + 1) - m * (m + 1)) * (spin.B_x - spin.B_y * 1j)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, -1):
                    hamiltonian[i, j] += (
                        1 / 2 * LANDE_FACTOR * MU_B * math.sqrt(s * (s + 1) - m * (m - 1)) * (spin.B_x + spin.B_y * 1j)
                    )

    return hamiltonian


def get_anisotropy_hamiltonian_matrix(spins: list[Spin], product_state_matrix: ProductStateMatrix) -> np.ndarray:
    """
    Generate the Hamiltonian matrix of the anisotropy term of spins
    with one main anisotropy axis using the product basis
    """

    number_of_spins = product_state_matrix.number_of_spins
    number_of_states = product_state_matrix.number_of_product_states

    hamiltonian = np.zeros([number_of_states, number_of_states]) * 1j

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            for spin_index in range(number_of_spins):
                spin = spins[spin_index]
                m = product_state_matrix.spin(spin_index)[j]
                s = product_state_matrix.spin_values[spin_index]

                if i == j:
                    hamiltonian[i, i] += spin.D * spin.e_D_z**2 * m**2
                    hamiltonian[i, i] += (
                        spin.D * (2 * s * (s + 1) - 2 * m**2) * (1 / 4 * spin.e_D_x**2 + 1 / 4 * spin.e_D_y**2)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, +1):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m + 1))
                        * (2 * m + 1)
                        * (1 / 2 * spin.e_D_x * spin.e_D_z - 1j / 2 * spin.e_D_y * spin.e_D_z)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, -1):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m - 1))
                        * (2 * m - 1)
                        * (1 / 2 * spin.e_D_x * spin.e_D_z + 1j / 2 * spin.e_D_y * spin.e_D_z)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, +2):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m + 1))
                        * math.sqrt(s * (s + 1) - (m + 1) * (m + 2))
                        * (1 / 4 * spin.e_D_x**2 - 1 / 4 * spin.e_D_y**2 - 1j / 2 * spin.e_D_x * spin.e_D_y)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_index, -2):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m - 1))
                        * math.sqrt(s * (s + 1) - (m - 1) * (m - 2))
                        * (1 / 4 * spin.e_D_x**2 - 1 / 4 * spin.e_D_y**2 + 1j / 2 * spin.e_D_x * spin.e_D_y)
                    )

    return hamiltonian
