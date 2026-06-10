import numpy as np

from alignment import calculate_alignment
from magnetization import calculate_magnetization_from_spin_expectation_values
from results import Results

from math_helper import number


class OrderGenerator:
    """"""

    def __init__(self, results: Results):
        self.overlap_weight = 0
        self.spin_expectation_weight = 0
        self.magnetization_weight = 0
        self.alignment_weight = 0
        self.continuity_weight = 1

        self.state_ordering_matrix = self.generate_state_order_matrix(results)

    def set_weights(
        self,
        overlap: number,
        spin_expectation: number,
        magnetization: number,
        alignment: number,
        continuity: number,
    ) -> None:
        self.overlap_weight = overlap
        self.spin_expectation_weight = spin_expectation
        self.magnetization_weight = magnetization
        self.alignment_weight = alignment
        self.continuity_weight = continuity

    def generate_state_order_matrix(self, results: Results) -> np.ndarray:
        eigenvalues = results.eigenvalues
        eigenvectors = results.eigenvectors
        x_values = results.x_values
        number_of_x_values, number_of_states = eigenvalues.shape
        state_ordering_matrix = -np.ones([number_of_x_values, number_of_states])
        number_of_spins = results.product_state_matrix.number_of_spins
        spin_expectation_values = results.spin_expectation_values

        if number_of_x_values == 0:
            return state_ordering_matrix

        state_ordering_matrix[0] = np.array(range(number_of_states))

        for k in range(1, number_of_x_values):
            #

            cost_matrix = np.empty((number_of_states, number_of_states)) * 0j
            for i in range(number_of_states):
                for j in range(number_of_states):
                    #

                    old_i = int(state_ordering_matrix[k - 1, i])
                    cost = 0

                    if self.continuity_weight > 0:
                        if k == 1:
                            cost += self.continuity_weight * abs(eigenvalues[k - 1, old_i] - eigenvalues[k, j])
                        else:
                            older_i = int(state_ordering_matrix[k - 2, old_i])
                            slope = (eigenvalues[k - 1, old_i] - eigenvalues[k - 2, older_i]) / (
                                x_values[k - 1] - x_values[k - 2]
                            )
                            predicted_next_eigenvalue = eigenvalues[k - 1, old_i] + slope * (
                                x_values[k] - x_values[k - 1]
                            )
                            cost += self.continuity_weight * abs(
                                4
                                * (predicted_next_eigenvalue - eigenvalues[k, j])
                                / (eigenvalues[k, number_of_states - 1] - eigenvalues[k, 0])
                            )

                    if self.spin_expectation_weight > 0 and spin_expectation_values is not None:
                        spin_expectation_i = np.zeros(3 * number_of_spins) * 0j
                        spin_expectation_j = np.zeros(3 * number_of_spins) * 0j
                        for spin in range(number_of_spins):
                            spin_expectation_i[spin : spin + 3] += spin_expectation_values[k - 1, old_i, spin]
                            spin_expectation_j[spin : spin + 3] += spin_expectation_values[k, j, spin]
                        cost += (
                            self.spin_expectation_weight
                            * np.linalg.norm((spin_expectation_i - spin_expectation_j) / results.spin_rings[k].spin)
                            ** 2
                        )

                    if self.magnetization_weight > 0 and spin_expectation_values is not None:
                        magnetization_i = 0j
                        magnetization_j = 0j
                        for spin in range(number_of_spins):
                            magnetization_i += calculate_magnetization_from_spin_expectation_values(
                                spins=results.spin_rings[k - 1].spins,
                                spin_expectation_values=spin_expectation_values[k - 1],
                                eigenvalue_index=old_i,
                            )
                            magnetization_j += calculate_magnetization_from_spin_expectation_values(
                                spins=results.spin_rings[k].spins,
                                spin_expectation_values=spin_expectation_values[k],
                                eigenvalue_index=j,
                            )
                        cost += self.magnetization_weight * (magnetization_i - magnetization_j) ** 2

                    if self.alignment_weight > 0 and spin_expectation_values is not None:
                        alignment_i = 0j
                        alignment_j = 0j
                        alignment_i += calculate_alignment(
                            spins=results.spin_rings[k - 1].spins,
                            product_state_matrix=results.product_state_matrix,
                            eigenvalue_index=old_i,
                            eigenvectors=eigenvectors[k - 1],
                        )
                        alignment_j += calculate_alignment(
                            spins=results.spin_rings[k].spins,
                            product_state_matrix=results.product_state_matrix,
                            eigenvalue_index=j,
                            eigenvectors=eigenvectors[k],
                        )
                        cost += self.alignment_weight * (alignment_i - alignment_j) ** 2

                    e_vec_i: np.ndarray = eigenvectors[k - 1, :, old_i]
                    e_vec_j: np.ndarray = eigenvectors[k, :, j]
                    cost += self.overlap_weight * (1 - np.abs(e_vec_i.conj() @ e_vec_j)) ** 2

                    cost_matrix[i, j] = cost

            for i in range(number_of_states):
                order = np.argsort(cost_matrix[i])
                for j in order:
                    if j not in state_ordering_matrix[k]:
                        state_ordering_matrix[k, i] = j
                        break

        return state_ordering_matrix
