from abc import ABC, abstractmethod

import numpy as np

from math_helper import number
from results import Results


class Plotter(ABC):
    """Common interface for plotters that collect result data and write figures."""

    STATES_LABEL = r"$\nu=${eigenvalue_index}"

    def _get_label_order_x_index(self, x_values: np.ndarray, label_order_x_value: number | None) -> int:
        if len(x_values) == 0:
            raise ValueError("Cannot build plot labels without x values.")
        if label_order_x_value is None:
            return 0
        return int(np.argmin(np.abs(x_values - label_order_x_value)))

    def _get_color_values_below_cutoff(self, color_map: np.ndarray, number_of_shown_states: int) -> list[int]:
        return [int(color_value) for color_value in np.unique(color_map[:, :number_of_shown_states])]

    def _get_state_labels_and_colors(
        self,
        x_values: np.ndarray,
        color_map: np.ndarray,
        number_of_shown_states: int,
        label_order_x_value: number | None,
    ) -> tuple[list[str], list[int]]:
        x_index = self._get_label_order_x_index(x_values, label_order_x_value)
        color_values = self._get_color_values_below_cutoff(color_map, number_of_shown_states)
        state_indices_at_label_x = {
            int(color_value): eigenvalue_index for eigenvalue_index, color_value in enumerate(color_map[x_index])
        }
        color_values.sort(key=lambda color_value: state_indices_at_label_x[color_value])
        labels = [
            self.STATES_LABEL.format(eigenvalue_index=state_indices_at_label_x[color_value])
            for color_value in color_values
        ]
        return labels, color_values

    @abstractmethod
    def add_points(
        self,
        results: Results,
        color_map: np.ndarray,
        label_order_x_value: number | None = None,
    ) -> None: ...

    @abstractmethod
    def save(self, folder: str) -> None: ...
