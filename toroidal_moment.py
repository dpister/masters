import math

import numpy as np

from product_states import ProductStateMatrix
from spin import SpinRing


def get_toroidal_moment(
    spin_ring: SpinRing,
    eigenvalue_index: int,
    product_state_matrix: ProductStateMatrix,
    eigenvectors: np.ndarray
) -> np.ndarray:
    
    s = product_state_matrix.spin_value
    N = number_of_spins = product_state_matrix.number_of_spins
    number_of_states = int(2*s+1)**N

    result = np.zeros(3) * 1j
    
    for i in range(number_of_states):
        for j in range(number_of_states):

            for spin_ind in range(number_of_spins):
                m = product_state_matrix.spin(spin_ind)[j]
                c_i: complex = eigenvectors[i, eigenvalue_index]
                c_j: complex = eigenvectors[j, eigenvalue_index]
                spin = spin_ring.spins[spin_ind]

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_ind, +1):
                    result[0] += 1j/2 * spin.r_z * c_i.conjugate() * c_j * math.sqrt(s*(s+1) - m*(m+1))
                    result[1] += 1/2 * spin.r_z * c_i.conjugate() * c_j * math.sqrt(s*(s+1) - m*(m+1))
                    result[2] += (-1j/2 * spin.r_x - 1/2 * spin.r_y) * c_i.conjugate() * c_j * math.sqrt(s*(s+1) - m*(m+1))

                if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin_ind, -1):
                    result[0] += -1j/2 * spin.r_z * c_i.conjugate() * c_j * math.sqrt(s*(s+1) - m*(m-1))
                    result[1] += 1/2 * spin.r_z * c_i.conjugate() * c_j * math.sqrt(s*(s+1) - m*(m-1))
                    result[2] += (1j/2 * spin.r_x - 1/2 * spin.r_y) * c_i.conjugate() * c_j * math.sqrt(s*(s+1) - m*(m+1))

                if i==j:
                    result[0] += spin.r_y * m * c_i.conjugate() * c_j
                    result[1] += -spin.r_x * m * c_i.conjugate() * c_j

    return result