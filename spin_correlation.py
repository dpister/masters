import math

import numpy as np

from product_states import ProductStateMatrix


def get_spin_correlation(
        spin1_index: int, 
        spin2_index: int, 
        eigenvalue_index: int,
        product_state_matrix: ProductStateMatrix, 
        eigenvectors: np.ndarray
) -> complex:
    
    s = product_state_matrix.spin_value
    N = product_state_matrix.number_of_spins
    number_of_states = int(2*s+1)**N

    result = 0j
    
    if spin1_index == spin2_index:
        raise Exception("choose 2 different spins")
    
    for i in range(number_of_states):
        for j in range(number_of_states):

            m1 = product_state_matrix.spin(spin1_index)[j]
            m2 = product_state_matrix.spin(spin2_index)[j]
            c_i: complex = eigenvectors[i, eigenvalue_index]
            c_j: complex = eigenvectors[j, eigenvalue_index]
            
            if i == j:
                result += m1 * m2 * c_i.conjugate() * c_j

            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin1_index, +1).changed(spin2_index, -1):
                result += 1/2 * math.sqrt(s*(s+1) - m1*(m1+1)) * math.sqrt(s*(s+1) - m2*(m2-1)) * c_i.conjugate() * c_j

            if product_state_matrix.state(i) == product_state_matrix.state(j).changed(spin1_index, -1).changed(spin2_index, +1):
                result += 1/2 * math.sqrt(s*(s+1) - m1*(m1-1)) * math.sqrt(s*(s+1) - m2*(m2+1)) * c_i.conjugate() * c_j

    return result

        