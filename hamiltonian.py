import math

import numpy as np

from math_helper import BOHR_MAGNETON
from product_states import ProductStateMatrix
from spin import SpinRing


def get_heisenberg_interaction_hamiltonian_matrix(
    spin_ring: SpinRing, product_state_matrix: ProductStateMatrix
) -> np.ndarray:
    """
    generate the Hamiltonian matrix for the Heisenberg interaction
    of a spin ring using the product basis
    """

    N = number_of_spins = spin_ring.number_of_spins
    s = spin_ring.spin
    J = spin_ring.heisenberg_interaction_matrix
    number_of_states = int(2 * s + 1) ** N

    hamiltonian = np.zeros([number_of_states, number_of_states]) * 1j

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            for spin1 in range(number_of_spins):
                mk = product_state_matrix.spin(spin1)[j]

                for spin2 in range(spin1):
                    ml = product_state_matrix.spin(spin2)[j]

                    if i == j:
                        hamiltonian[i, i] += mk * ml * J[spin1, spin2]

                    if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                        spin1, +1
                    ).changed(spin2, -1):
                        hamiltonian[i, j] += (
                            J[spin1, spin2]
                            / 2
                            * math.sqrt(s * (s + 1) - mk * (mk + 1))
                            * math.sqrt(s * (s + 1) - ml * (ml - 1))
                        )

                    if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                        spin1, -1
                    ).changed(spin2, +1):
                        hamiltonian[i, j] += (
                            J[spin1, spin2]
                            / 2
                            * math.sqrt(s * (s + 1) - mk * (mk - 1))
                            * math.sqrt(s * (s + 1) - ml * (ml + 1))
                        )

    return hamiltonian


def get_zeeman_hamiltonian_matrix(
    spin_ring: SpinRing, product_state_matrix: ProductStateMatrix
) -> np.ndarray:
    """generate the Hamiltonian matrix of the Zeeman term of a spin ring using the product basis"""

    N = number_of_spins = spin_ring.number_of_spins
    s = spin_ring.spin
    MU_B = BOHR_MAGNETON
    number_of_states = int(2 * s + 1) ** N

    hamiltonian = np.zeros([number_of_states, number_of_states]) * 1j

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            for spin_index in range(number_of_spins):
                spin = spin_ring.spins[spin_index]
                m = product_state_matrix.spin(spin_index)[j]

                if i == j:
                    hamiltonian[i, j] += 2 * MU_B * m * spin.B_z

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                    spin_index, +1
                ):
                    hamiltonian[i, j] += (
                        MU_B * math.sqrt(s * (s + 1) - m * (m + 1)) * (spin.B_x - spin.B_y * 1j)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                    spin_index, -1
                ):
                    hamiltonian[i, j] += (
                        MU_B * math.sqrt(s * (s + 1) - m * (m - 1)) * (spin.B_x + spin.B_y * 1j)
                    )

    return hamiltonian


def get_anisotropy_hamiltonian_matrix(
    spin_ring: SpinRing, product_state_matrix: ProductStateMatrix
) -> np.ndarray:
    """
    generate the Hamiltonian matrix of the anisotropy term of a spin ring
    with one main anisotropy axis using the product basis
    """

    N = number_of_spins = spin_ring.number_of_spins
    s = spin_ring.spin
    number_of_states = int(2 * s + 1) ** N

    hamiltonian = np.zeros([number_of_states, number_of_states]) * 1j

    for i in range(number_of_states):
        for j in range(number_of_states):
            #

            for spin_index in range(number_of_spins):
                spin = spin_ring.spins[spin_index]
                m = product_state_matrix.spin(spin_index)[j]

                if i == j:
                    hamiltonian[i, i] += spin.D * spin.D_z**2 * m**2
                    hamiltonian[i, i] += (
                        spin.D
                        * (2 * s * (s + 1) - 2 * m**2)
                        * (1 / 4 * spin.D_x**2 + 1 / 4 * spin.D_y**2)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                    spin_index, +1
                ):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m + 1))
                        * (2 * m + 1)
                        * (1 / 2 * spin.D_x * spin.D_z - 1j / 2 * spin.D_y * spin.D_z)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                    spin_index, -1
                ):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m - 1))
                        * (2 * m - 1)
                        * (1 / 2 * spin.D_x * spin.D_z + 1j / 2 * spin.D_y * spin.D_z)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                    spin_index, +2
                ):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m + 1))
                        * math.sqrt(s * (s + 1) - (m + 1) * (m + 2))
                        * (1 / 4 * spin.D_x**2 - 1 / 4 * spin.D_y**2 - 1j / 2 * spin.D_x * spin.D_y)
                    )

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(
                    spin_index, -2
                ):
                    hamiltonian[i, j] += (
                        spin.D
                        * math.sqrt(s * (s + 1) - m * (m - 1))
                        * math.sqrt(s * (s + 1) - (m - 1) * (m - 2))
                        * (1 / 4 * spin.D_x**2 - 1 / 4 * spin.D_y**2 + 1j / 2 * spin.D_x * spin.D_y)
                    )

    return hamiltonian
