from __future__ import annotations
import itertools
import numpy as np
from numpy.polynomial.polynomial import Polynomial

from math_helper import number


class OrderGenerator:
    """"""

    def __init__(
        self,
        x_values: np.ndarray,
        eigenvalues: np.ndarray[tuple[int, int], np.dtype[np.float64]],
        eigenvectors: np.ndarray,
    ):
        self.x_values = x_values
        self.eigenvectors = eigenvectors
        self.eigenvalues = eigenvalues
        self.eigenvectors = self.eigenvectors
        self.observables: list[np.ndarray] = []

        self.overlap_weight = 0
        self.observable_weights: list[number] = []
        self.continuity_weight = 0
        self.interpolation_weight = 0

        self.number_of_x_values, self.number_of_states = eigenvalues.shape
        self._state_ordering = -np.ones([self.number_of_x_values, self.number_of_states], dtype=np.int_)

    def reset(self) -> OrderGenerator:
        self.observables: list[np.ndarray] = []
        self.overlap_weight = 0
        self.observable_weights: list[number] = []
        self.continuity_weight = 0
        self.interpolation_weight = 0
        return self

    def with_state_overlap(self, weight: number = 1) -> OrderGenerator:
        self.overlap_weight = weight
        return self

    def with_observable(self, observable_values: np.ndarray, weight: number = 1) -> OrderGenerator:
        self.observables.append(observable_values)
        self.observable_weights.append(weight)
        return self

    def with_continuity(self, weight: number = 1) -> OrderGenerator:
        self.continuity_weight = weight
        return self

    def with_interpolation(self, weight: number = 1) -> OrderGenerator:
        self.interpolation_weight = weight
        return self

    def calculate_state_order(self) -> np.ndarray:
        if self.number_of_x_values == 0:
            return self._state_ordering
        self._state_ordering[0] = np.arange(self.number_of_states)

        for k in range(1, self.number_of_x_values):
            #

            cost_matrix = np.empty((self.number_of_states, self.number_of_states))

            for i in range(self.number_of_states):
                for j in range(self.number_of_states):
                    #

                    cost = 0
                    cost += self._calculate_continuity_cost(k, i, j)
                    cost += self._calculate_observable_cost(k, i, j)
                    cost += self._calculate_overlap_cost(k, i, j)
                    cost_matrix[i, j] = cost

            for i in range(self.number_of_states):
                state = self._pick_best_available_state(k, i, cost_matrix)
                self._state_ordering[k, i] = state

        return self._state_ordering

    def calculate_state_order_using_interpolation(self) -> np.ndarray:
        if self.number_of_x_values == 0:
            return self._state_ordering
        self._reverse_state_ordering = -np.ones([self.number_of_x_values, self.number_of_states], dtype=np.int_)
        self._reverse_state_ordering[0] = np.arange(self.number_of_states)
        self._state_ordering[0] = np.arange(self.number_of_states)

        for k in range(1, self.number_of_x_values):
            #
            for i in range(self.number_of_states):
                best_state = self.find_best_next_point_with_interpolation(k, i)
                self._reverse_state_ordering[k, best_state] = i
                self._state_ordering[k, i] = best_state

        return self._state_ordering

    def _pick_best_available_state(self, k: int, i: int, cost_matrix: np.ndarray) -> int:
        ordered_states = np.argsort(cost_matrix[i])
        for state in ordered_states:
            if state not in self._state_ordering[k]:
                return state
        return ordered_states[-1]

    def find_best_next_point_with_interpolation(self, k: int, i: int) -> int:

        assert self.number_of_x_values > 2
        ordered_i = self._state_ordering[k - 1, i]
        x_values_list: list[number] = []
        future_point_steps: list[list[int]] = []
        first_eigenvalues: list[number] = []
        deviations: list[number] = []
        curvature_changes: list[number] = []

        for offset in [-2, -1, 0, 1, 2]:
            if not 0 <= k + offset < self.number_of_x_values:
                continue
            x_values_list.append(self.x_values[k + offset])
            if offset < 0:
                first_eigenvalues.append(self.eigenvalues[k + offset, self._state_ordering[k + offset, i]])
            else:
                future_point_steps.append([-2, -1, 0, 1, 2])

        x_values = np.array(x_values_list)
        number_of_future_points = len(future_point_steps)
        product_indices: list[tuple[int, ...]] = []
        for indices in itertools.product(*future_point_steps):
            eigenvalues_list = first_eigenvalues[:]

            should_skip = False
            for offset in range(number_of_future_points):
                if not 0 <= ordered_i + indices[offset] < self.number_of_states:
                    should_skip = True
                    break
                eigenvalues_list.append(self.eigenvalues[k + offset, ordered_i + indices[offset]])

            if should_skip:
                continue

            product_indices.append(indices)

            eigenvalues = np.array(eigenvalues_list)
            deg = 2 if len(x_values) > 3 else 1
            polynomial, other = Polynomial.fit(
                x_values, eigenvalues, deg=deg, domain=[self.x_values[0], self.x_values[-1]], full=True
            )
            polynomial.convert()
            sum_of_squared_residuals = float(other[0][0])  # type: ignore
            curvature_change = 0 if polynomial.degree() == 1 else 2 * polynomial.coef[2]
            curvature_changes.append(abs(curvature_change))
            deviations.append(sum_of_squared_residuals)

        deviation_threshold = 1e-7
        best_indices: list[int] = []
        for j, (deviation, curvature_change) in enumerate(zip(deviations, curvature_changes)):
            if deviation < deviation_threshold:
                best_indices.append(j)
        best_indices.sort(key=lambda j: curvature_changes[j])

        while best_indices:
            j = best_indices.pop(0)
            indices = product_indices[j]
            state = ordered_i + indices[0]
            if state not in self._state_ordering[k]:
                return state

        raise ValueError(f"No matching state found found: x_index: {k}, state: {i}")

    def _calculate_continuity_cost(self, k: int, j: int, i: int) -> number:
        old_i = int(self._state_ordering[k - 1, i])
        cost = 0
        if self.continuity_weight > 0:
            if k == 1:
                cost = self.continuity_weight * abs(self.eigenvalues[k - 1, old_i] - self.eigenvalues[k, j])
                cost = self._rescale_continuity_cost(k, cost)
            else:
                older_i = int(self._state_ordering[k - 2, old_i])
                slope = (self.eigenvalues[k - 1, old_i] - self.eigenvalues[k - 2, older_i]) / (
                    self.x_values[k - 1] - self.x_values[k - 2]
                )
                predicted_next_eigenvalue = self.eigenvalues[k - 1, old_i] + slope * (
                    self.x_values[k] - self.x_values[k - 1]
                )
                cost = self.continuity_weight * abs(predicted_next_eigenvalue - self.eigenvalues[k, j])
                cost = self._rescale_continuity_cost(k, cost)
        return cost

    def _rescale_continuity_cost(self, k: int, cost: number) -> number:
        return 4 * cost / (self.eigenvalues[k, self.number_of_states - 1] - self.eigenvalues[k, 0])

    def _calculate_observable_cost(self, k: int, i: int, j: int) -> number:
        old_i = int(self._state_ordering[k - 1, i])
        cost = 0
        for observable_values, observable_weight in zip(self.observables, self.observable_weights):
            if observable_weight > 0:
                observable_i = observable_values[k, old_i]
                observable_j = observable_values[k, j]
                cost += observable_weight * np.linalg.norm(observable_i - observable_j) ** 2
        return cost  # type: ignore

    def _calculate_overlap_cost(self, k: int, i: int, j: int) -> number:
        old_i = int(self._state_ordering[k - 1, i])
        e_vec_i: np.ndarray = self.eigenvectors[k - 1, :, old_i]
        e_vec_j: np.ndarray = self.eigenvectors[k, :, j]
        return self.overlap_weight * (1 - abs(np.dot(e_vec_i.conj(), e_vec_j))) ** 2
