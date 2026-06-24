# import matplotlib

# better performance but can't show plots, only savefig
# yes, you have to put it here (before the matplotlib.pyplot import)
# matplotlib.use("Agg")


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.style as mplstyle

from math_helper import number


class Plot:
    """
    Wrapper class to simplify matplotblib calls by preapplying some default values or bundling calls.
    Manages a single figure and ax to minimize overhead.
    Also hides away the typing problems of matplotlib.
    """

    LEGEND_LABELSIZE = 13
    TICKSIZE = 12
    LABELSIZE = 15
    LINEWIDTH = 0
    WINDOWSIZE_X = 13
    WINDOWSIZE_Y = 7
    MARKER = "."
    TITLE_LOCATION = "center"
    LEGEND_LOCATION = "upper right"
    BBOX_INCHES = "tight"  # removes whitespace around plot when saving
    RASTERIZED = True  # boosts performance
    COLORMAP_NAME = "tab20"

    mplstyle.use("fast")

    def __init__(self):
        self.fig, self.ax = plt.subplots()  # type: ignore

    def configure(
        self,
        xlabel: str | None = None,
        ylabel: str | None = None,
        title: str | None = None,
        y_interval: tuple[number, number] | tuple[()] | None = None,
    ) -> None:
        self.ax.tick_params(axis="both", labelsize=self.TICKSIZE)  # type: ignore
        if xlabel is not None:
            self.ax.set_xlabel(xlabel, fontsize=self.LABELSIZE)  # type: ignore
        if ylabel is not None:
            self.ax.set_ylabel(ylabel, fontsize=self.LABELSIZE)  # type: ignore
        if title is not None:
            self.ax.set_title(title, fontsize=self.LABELSIZE)  # type: ignore
        if y_interval:
            self.ax.set_ylim(y_interval)

    def plot(
        self,
        xvalues: np.ndarray | number,
        yvalues: np.ndarray | number,
        color: str | None = None,
        color_values: np.ndarray | None = None,
    ) -> None:
        if color is not None and color_values is not None:
            raise Exception("Either set color or color_values, not both")
        if color_values is not None:
            self.ax.scatter(  # type: ignore
                xvalues,
                yvalues,
                c=self._get_colors_from_values(color_values),
                marker=self.MARKER,
                linewidths=self.LINEWIDTH,
                rasterized=self.RASTERIZED,
            )
        else:
            self.ax.scatter(  # type: ignore
                xvalues, yvalues, color=color, marker=self.MARKER, linewidths=self.LINEWIDTH, rasterized=self.RASTERIZED
            )

    def set_legend(self, labels: list[str] | None = None, color_values: list[int] | None = None) -> None:
        if labels is None:
            self.ax.legend(loc=self.LEGEND_LOCATION, fontsize=self.LEGEND_LABELSIZE)  # type: ignore
        elif color_values is None:
            self.ax.legend(labels=labels, loc=self.LEGEND_LOCATION, fontsize=self.LEGEND_LABELSIZE)  # type: ignore
        else:
            colormap = plt.get_cmap(self.COLORMAP_NAME)
            colors = self._get_colors_from_values(color_values)
            legend_elements = [
                Line2D([0], [0], marker=self.MARKER, linestyle="", color=color, label=label)
                for label, color in zip(labels, colors)
            ]
            self.ax.legend(handles=legend_elements, loc=self.LEGEND_LOCATION, fontsize=self.LEGEND_LABELSIZE)  # type: ignore

    def _get_colors_from_values(self, color_values: np.ndarray | list[int]) -> list[tuple[float, float, float, float]]:
        colormap = plt.get_cmap(self.COLORMAP_NAME)
        return [colormap(int(color_value)) for color_value in np.asarray(color_values).ravel()]

    def save(self, path: str) -> None:
        self.fig.savefig(path, bbox_inches=self.BBOX_INCHES)  # type: ignore
