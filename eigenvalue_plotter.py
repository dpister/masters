import os

import numpy as np

from math_helper import flatten
from plotter import Plotter
from results import Results
from subplots import Plot


class EigenvaluePlotter(Plotter):
    """Plots the lowest eigenvalues and/or all eigenvalues of a hamiltonian matrix."""

    IMAGE_PATH = "low_eigenvalues.png"
    IMAGE_PATH_LOW = "all_eigenvalues.png"
    YLABEL = r"$E_\nu$ in K"
    TITLE = "Eigenwerte $E_\\nu$"
    TITLE_LOW = "Unterste Eigenwerte $E_\\nu$"

    def __init__(
        self,
        number_of_shown_states: int,
        xlabel: str,
        title_subinfo: str,
        y_interval: tuple[int, int] | tuple[()],
        y_interval_low: tuple[int, int] | tuple[()],
    ):
        self.plot = Plot()
        self.plot_low = Plot()
        self.number_of_shown_states = number_of_shown_states
        full_title = self.TITLE + "\n" + title_subinfo
        full_title_low = self.TITLE_LOW + "\n" + title_subinfo
        self.plot.configure(
            xlabel=xlabel,
            title=full_title,
            y_interval=y_interval,
            ylabel=self.YLABEL,
        )
        self.plot_low.configure(
            xlabel=xlabel,
            title=full_title_low,
            y_interval=y_interval_low,
            ylabel=self.YLABEL,
        )

    def add_points(
        self,
        results: Results,
        color_map: np.ndarray,
    ) -> None:
        new_x_values, new_eigenvalues = flatten(results.x_values, results.eigenvalues[:, : self.number_of_shown_states])
        _, new_color_map = flatten(results.x_values, color_map[:, : self.number_of_shown_states])
        self.plot_low.plot(new_x_values, new_eigenvalues, color_values=new_color_map)
        self.plot.plot(new_x_values, new_eigenvalues, color_values=new_color_map)

    def save(self, folder: str) -> None:
        path = os.path.join(folder, self.IMAGE_PATH)
        self.plot.save(path)
        path = os.path.join(folder, self.IMAGE_PATH_LOW)
        self.plot_low.save(path)
