from __future__ import annotations
from dataclasses import dataclass
import itertools
import numpy as np
from numpy.polynomial.polynomial import Polynomial

from math_helper import number


class OrderGenerator:
    """"""

    def __init__(self, x_values: np.ndarray, eigenvalues: np.ndarray):
        self.x_values = x_values
        self.eigenvalues = eigenvalues
        self.number_of_x_values, self.number_of_states = eigenvalues.shape
        self.reset_state_ordering()

    def reset_state_ordering(self) -> None:
        self._state_ordering = -np.ones([self.number_of_x_values, self.number_of_states], dtype=np.int_)
        self._reversed_state_ordering = -np.ones([self.number_of_x_values, self.number_of_states], dtype=np.int_)
        if self.number_of_x_values != 0:
            self._state_ordering[0] = np.arange(self.number_of_states)
            self._reversed_state_ordering[0] = np.arange(self.number_of_states)

    def get_state_ordering(self) -> np.ndarray:
        return self._state_ordering

    def get_reversed_state_ordering(self) -> np.ndarray:
        return self._reversed_state_ordering

    def calculate_state_order_using_overlap(self, eigenvectors: np.ndarray) -> np.ndarray:
        self.reset_state_ordering()
        for k in range(1, self.number_of_x_values):
            for state in range(self.number_of_states):
                best_new_state = self._find_best_state_using_overlap(k, state, eigenvectors)
                self._state_ordering[k, best_new_state] = state
                self._reversed_state_ordering[k, state] = best_new_state
        return self._state_ordering

    def _find_best_state_using_overlap(self, x_index: int, state: int, eigenvectors: np.ndarray) -> int:
        costs = np.empty(self.number_of_states)
        old_state = int(self._reversed_state_ordering[x_index - 1, state])
        e_vec_i: np.ndarray = eigenvectors[x_index - 1, :, old_state]
        for new_state in range(self.number_of_states):
            e_vec_j: np.ndarray = eigenvectors[x_index, :, new_state]
            cost = 1 - abs(np.dot(e_vec_i.conj(), e_vec_j))
            costs[new_state] = cost
        return self._pick_best_available_state(x_index, costs)

    def _pick_best_available_state(self, x_index: int, costs: np.ndarray) -> int:
        ordered_states = np.argsort(costs)
        for state in ordered_states:
            if state not in self._reversed_state_ordering[x_index]:
                return state
        raise ValueError(f"No matching state found: x_index: {x_index}")

    def calculate_state_order_using_interpolation(self) -> np.ndarray:
        self.reset_state_ordering()
        for k in range(1, self.number_of_x_values):
            #
            if k == 1:
                self._state_ordering[1] = np.arange(self.number_of_states)
                self._reversed_state_ordering[1] = np.arange(self.number_of_states)
                continue

            for state in range(self.number_of_states):
                best_new_state = self._find_best_next_point_with_interpolation(k, state)
                self._state_ordering[k, best_new_state] = state
                self._reversed_state_ordering[k, state] = best_new_state

        return self._state_ordering

    def _find_best_next_point_with_interpolation(self, x_index: int, state: int) -> int:
        costs = np.empty(self.number_of_states)
        for new_state in range(self.number_of_states):
            if x_index == 2:
                predicted_next_eigenvalue = self._calculate_interpolation_1st_degree(x_index, state)
            else:
                predicted_next_eigenvalue = self._calculate_interpolation_2nd_degree(x_index, state)
            cost = abs(predicted_next_eigenvalue - self.eigenvalues[x_index, new_state])
            costs[new_state] = cost
        return self._pick_best_available_state(x_index, costs)

    def _calculate_interpolation_1st_degree(self, x_index: int, state: int) -> number:
        x0 = self.x_values[x_index - 2]
        x1 = self.x_values[x_index - 1]
        y0 = self._get_eigenvalue_from_ordered_state(x_index - 2, state)
        y1 = self._get_eigenvalue_from_ordered_state(x_index - 1, state)
        x = self.x_values[x_index]
        slope = (y1 - y0) / (x1 - x0)
        predicted_next_eigenvalue = y0 + slope * (x - x0)
        return predicted_next_eigenvalue

    def _calculate_interpolation_2nd_degree(self, x_index: int, state: int) -> number:
        x0 = self.x_values[x_index - 3]
        x1 = self.x_values[x_index - 2]
        x2 = self.x_values[x_index - 1]
        x = self.x_values[x_index]
        y0 = self._get_eigenvalue_from_ordered_state(x_index - 3, state)
        y1 = self._get_eigenvalue_from_ordered_state(x_index - 2, state)
        y2 = self._get_eigenvalue_from_ordered_state(x_index - 1, state)
        predicted_next_eigenvalue = 0
        predicted_next_eigenvalue += y0 * (x - x1) * (x - x2) / ((x0 - x1) * (x0 - x2))
        predicted_next_eigenvalue += y1 * (x - x0) * (x - x2) / ((x1 - x0) * (x1 - x2))
        predicted_next_eigenvalue += y2 * (x - x0) * (x - x1) / ((x2 - x0) * (x2 - x1))
        return predicted_next_eigenvalue

    def calculate_state_order_using_fitting(self) -> np.ndarray:
        self.reset_state_ordering()
        for x_index in range(1, self.number_of_x_values):
            for state in range(self.number_of_states):
                best_new_state = self._find_best_next_point_with_fitting(x_index, state)
                self._reversed_state_ordering[x_index, state] = best_new_state
                self._state_ordering[x_index, best_new_state] = state
        return self._state_ordering

    def _find_best_next_point_with_fitting(
        self, x_index: int, state: int, number_of_candidates_up_and_down: int = 2
    ) -> int:
        ordered_state = self._reversed_state_ordering[x_index - 1, state]
        x_values, past_eigenvalues, candidate_offsets = self._build_fitting_window(
            x_index, state, number_of_candidates_up_and_down
        )

        candidate_paths = self._generate_candidate_paths(x_index, ordered_state, past_eigenvalues, candidate_offsets)
        candidates = [self._fit_candidate_path(cp, x_values) for cp in candidate_paths]
        scored_candidates = sorted(candidates, key=lambda c: c.deviation)

        for candidate in scored_candidates:
            best_new_state = ordered_state + candidate.path.offsets[0]
            if best_new_state not in self._reversed_state_ordering[x_index]:
                return best_new_state

        raise ValueError(f"No matching state found: {x_index=} {state=}")

    def _get_eigenvalue_from_ordered_state(self, x_index: int, state: int) -> number:
        return self.eigenvalues[x_index, self._reversed_state_ordering[x_index, state]]

    def _get_future_point_steps(self, number_of_candidates_up_and_down: int) -> tuple[int, ...]:
        return tuple(range(-number_of_candidates_up_and_down, number_of_candidates_up_and_down + 1))

    def _build_fitting_window(
        self, x_index: int, state: int, number_of_candidates: int
    ) -> tuple[list[number], list[number], list[tuple[int, ...]]]:
        x_values: list[number] = []
        past_eigenvalues: list[number] = []
        future_offsets: list[tuple[int, ...]] = []

        for step in (-2, -1, 0, 1, 2):
            future_x = x_index + step

            if not (0 <= future_x < self.number_of_x_values):
                continue

            x_values.append(self.x_values[future_x])
            if step < 0:
                past_eigenvalues.append(self._get_eigenvalue_from_ordered_state(future_x, state))
            else:
                future_offsets.append(self._get_future_point_steps(number_of_candidates))

        return x_values, past_eigenvalues, future_offsets

    @dataclass(frozen=True)
    class CandidatePath:
        offsets: tuple[int, ...]
        eigenvalues: list[number]

    @dataclass(frozen=True)
    class Candidate:
        path: OrderGenerator.CandidatePath
        polynomial: Polynomial
        deviation: number
        curvature_change: number

    def _generate_candidate_paths(
        self,
        x_index: int,
        ordered_state: int,
        past_eigenvalues: list[number],
        candidate_offsets: list[tuple[int, ...]],
    ) -> list[CandidatePath]:

        candidates: list[OrderGenerator.CandidatePath] = []
        for offsets in itertools.product(*candidate_offsets):
            eigenvalues = past_eigenvalues.copy()
            valid = True

            for step, offset in enumerate(offsets):
                candidate_state = ordered_state + offset
                if not (0 <= candidate_state < self.number_of_states):
                    valid = False
                    break
                eigenvalues.append(self.eigenvalues[x_index + step, candidate_state])
            if valid:
                candidates.append(self.CandidatePath(offsets=offsets, eigenvalues=eigenvalues))

        return candidates

    def _fit_candidate_path(self, candidate_path: CandidatePath, x_values: list[number]) -> Candidate:
        degree = min(2, len(x_values) - 1)
        polynomial, other = Polynomial.fit(
            x_values, candidate_path.eigenvalues, deg=degree, full=True, domain=(self.x_values[0], self.x_values[-1])
        )
        sum_of_squared_residuals = float(other[0][0]) if len(other) and len(other[0]) else 0.0  # type: ignore
        curvature_change = 0 if polynomial.degree() == 1 else 2 * polynomial.coef[2]
        candidate = self.Candidate(
            path=candidate_path,
            polynomial=polynomial,
            deviation=sum_of_squared_residuals,
            curvature_change=curvature_change,
        )
        return candidate
