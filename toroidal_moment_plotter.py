import os

import numpy as np

from plotter import Plotter
from results import Results
from subplots import Plot
from math_helper import flatten, number, indices_mapping


class ToroidalMomentPlotter(Plotter):
    """"""

    IMAGE_PATH = "tor_moment_{direction}_expval.png"
    IMAGE_PATH_THERMAL = "tor_moment_{direction}_expval_thermal.png"
    YLABEL = "$<\\hat{{\\tau}}^{direction}>_\\nu$ in a.u."
    TITLE = "$<\\hat{{\\tau}}^{direction}>_\\nu$"
    YLABEL_THERMAL = "$<\\hat{{\\tau}}^{direction}>(T)$ in a.u."
    TITLE_THERMAL = "$<\\hat{{\\tau}}^{direction}>(T)$"

    TEMPERATURE_LABEL = "$T=${temperature} K"
    STATES_LABEL = "$\nu=${eigenvalue_index}"

    def __init__(
        self,
        number_of_shown_states: int,
        temperatures: list[number],
        xlabel: str,
        title_subinfo: str,
        y_intervals: dict[str, tuple[int, int] | tuple[()]],
        y_intervals_thermal: dict[str, tuple[int, int] | tuple[()]],
    ):
        self.plots = {"x": Plot(), "y": Plot(), "z": Plot()}
        self.thermal_plots = {"x": Plot(), "y": Plot(), "z": Plot()}
        self.number_of_shown_states = number_of_shown_states
        self.temperatures = temperatures

        for direction, plot in self.plots.items():
            full_title = self.TITLE.format(direction=direction) + "\n" + title_subinfo
            plot.configure(
                xlabel=xlabel,
                title=full_title,
                y_interval=y_intervals[direction],
                ylabel=self.YLABEL.format(direction=direction),
            )

        for direction, plot in self.thermal_plots.items():
            full_title = self.TITLE_THERMAL.format(direction=direction) + "\n" + title_subinfo
            plot.configure(
                xlabel=xlabel,
                title=full_title,
                y_interval=y_intervals_thermal[direction],
                ylabel=self.YLABEL.format(direction=direction),
            )

    def add_points(self, results: Results, color_map: np.ndarray) -> None:

        if results.toroidal_moments is not None:
            for direction, plot in self.plots.items():
                i = indices_mapping[direction]
                toroidal_moments = results.toroidal_moments[:, : self.number_of_shown_states, i]
                new_x_values, new_toroidal_moments = flatten(results.x_values, toroidal_moments)
                plot.plot(new_x_values, new_toroidal_moments, color_values=color_map[:, : self.number_of_shown_states])

        if results.toroidal_moments_thermal is not None:
            number_of_temperatures = len(results.temperatures)
            number_of_x_values = len(results.x_values)
            temperature_color_map = np.array([range(number_of_temperatures)] * number_of_x_values)
            for direction, plot in self.thermal_plots.items():
                i = indices_mapping[direction]
                thermals: np.ndarray = results.toroidal_moments_thermal[:, :, i]
                new_x_values, new_thermals = flatten(results.x_values, thermals)
                plot.plot(new_x_values, new_thermals, color_values=temperature_color_map)

    def save(self, folder: str) -> None:
        for direction, subplot in self.plots.items():
            path = os.path.join(folder, self.IMAGE_PATH.format(direction=direction))
            subplot.save(path)
        for direction, subplot in self.thermal_plots.items():
            path = os.path.join(folder, self.IMAGE_PATH_THERMAL.format(direction=direction))
            subplot.save(path)
