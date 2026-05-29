from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from math_helper import number
from config import config


class Subplot:
    """
    Wrapper class to combine Figures and Axes
    and to simplify matplotblib calls by preapplying some default values or bundling calls.
    Also hides away the ugly typing of matplotlib.
    """

    def __init__(self):
        self.fig, self.ax = plt.subplots()  # type: ignore

    def set_title(self, template_string: str, **kwargs: dict[str, Any]) -> None:
        title = template_string.format(**kwargs)
        return self.ax.set_title(title)  # type: ignore

    def configure(
        self,
        xlabel: str,
        ylabel: str,
        y_interval: tuple[number, number],
        title: str | None = None,
        labelsize: int = config["plot"]["labelsize"],
        ticksize: int = config["plot"]["ticksize"],
    ) -> None:
        if title is not None:
            self.ax.set_title(title, fontsize=labelsize)  # type: ignore
        self.ax.set_xlabel(xlabel, fontsize=labelsize)  # type: ignore
        self.ax.set_ylabel(ylabel, fontsize=labelsize)  # type: ignore
        self.ax.tick_params(axis="both", labelsize=ticksize)  # type: ignore
        self.ax.set_ylim(y_interval)

    def plot(
        self,
        xvalues: np.ndarray | number,
        yvalues: np.ndarray | number,
        color: str = config["plot"]["default_color"],
        marker: str = config["plot"]["marker"],
        linewidth: number = config["plot"]["linewidth"],
    ) -> None:
        self.ax.scatter(  # type: ignore
            xvalues, yvalues, color=color, marker=marker, linewidths=linewidth
        )

    def set_legend(
        self,
        labels: list[str],
        location: str = config["plot"]["legend_location"],
        legendsize: int = config["plot"]["legendsize"],
    ) -> None:
        self.ax.legend(labels, loc=location, fontsize=legendsize)  # type: ignore

    def save(
        self,
        save_path: str,
        should_trim: bool = config["plot"]["should_trim_whitespace_around_plot"],
        **kwargs: dict[str, Any],
    ) -> None:
        bbox_inches = "tight" if should_trim else None
        save_path_formatted = save_path.format(**kwargs)
        self.fig.savefig(save_path_formatted, bbox_inches=bbox_inches)  # type: ignore
