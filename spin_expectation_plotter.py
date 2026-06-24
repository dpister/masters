import os

import numpy as np

from math_helper import flatten, number, indices_mapping


from plotter import Plotter
from results import Results
from subplots import Plot


class SpinExpectationPlotter(Plotter):
    """Builds and saves plots for spin expectation values by spin and direction."""

    IMAGE_PATH = "spin{spin_index}_dir_{direction}_spin_expval.png"
    IMAGE_PATH_THERMAL = "spin{spin_index}_dir_{direction}_spin_thermal_expval.png"
    YLABEL = TITLE = "$<\\hat{{s}}^{direction}_{spin_index}>_\\nu$"
    YLABEL_THERMAL = TITLE_THERMAL = "$<\\hat{{s}}^{direction}_{spin_index}>(T)$"

    def __init__(
        self,
        number_of_shown_states: int,
        temperatures: list[number],
        number_of_spins: int,
        xlabel: str,
        title_subinfo: str,
        y_intervals: dict[str, tuple[int, int] | tuple[()]],
        y_intervals_thermal: dict[str, tuple[int, int] | tuple[()]],
    ):
        self.plots = [{"x": Plot(), "y": Plot(), "z": Plot()} for _ in range(number_of_spins)]
        self.thermal_plots = [{"x": Plot(), "y": Plot(), "z": Plot()} for _ in range(number_of_spins)]
        self.number_of_shown_states = number_of_shown_states
        self.temperatures = temperatures

        for spin_index, plots in enumerate(self.plots):
            for direction, plot in plots.items():
                full_title = self.TITLE.format(direction=direction, spin_index=spin_index) + "\n" + title_subinfo
                plot.configure(
                    xlabel=xlabel,
                    title=full_title,
                    y_interval=y_intervals[direction],
                    ylabel=self.YLABEL.format(direction=direction, spin_index=spin_index),
                )

        for spin_index, plots in enumerate(self.plots):
            for direction, plot in plots.items():
                full_title = (
                    self.TITLE_THERMAL.format(direction=direction, spin_index=spin_index) + "\n" + title_subinfo
                )
                plot.configure(
                    xlabel=xlabel,
                    title=full_title,
                    y_interval=y_intervals_thermal[direction],
                    ylabel=self.YLABEL_THERMAL.format(direction=direction, spin_index=spin_index),
                )

    def add_points(
        self, results: Results, color_map: np.ndarray, label_order_x_value: number | None = None
    ) -> None:
        if results.spin_expectation_values is None:
            return
        for spin_index, plots in enumerate(self.plots):
            for direction, plot in plots.items():
                i = indices_mapping[direction]
                new_x_values, new_spin_expectation_values = flatten(
                    results.x_values, results.spin_expectation_values[:, : self.number_of_shown_states, spin_index, i]
                )
                _, new_color_map = flatten(results.x_values, color_map[:, : self.number_of_shown_states])
                plot.plot(new_x_values, new_spin_expectation_values, color_values=new_color_map)
                labels, color_values = self._get_state_labels_and_colors(
                    results.x_values, color_map, self.number_of_shown_states, label_order_x_value
                )
                plot.set_legend(labels=labels, color_values=color_values)

    def save(self, folder: str) -> None:
        for spin_index, plots in enumerate(self.plots):
            for direction, plot in plots.items():
                path = os.path.join(folder, self.IMAGE_PATH.format(direction=direction, spin_index=spin_index))
                plot.save(path)
        for spin_index, plots in enumerate(self.thermal_plots):
            for direction, plot in plots.items():
                path = os.path.join(folder, self.IMAGE_PATH_THERMAL.format(direction=direction, spin_index=spin_index))
                plot.save(path)
