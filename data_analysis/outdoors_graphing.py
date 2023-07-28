import datetime

import matplotlib as mpl
from preprocessing import remove_null_points


class PlotOutdoorGraphs:
    def scatter_time_vs_distance(self, ax: mpl.axes.Axes, timing: list[datetime.datetime], distances: list[int], title="") -> None:
        """
        Plot a scatter plot of time against distance.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
            timing (list[datetime.datetime]): List of timings for each distance measured.
            distances (list[int]): List of distances measured by the sensor.
            title (str, optional): Title of the graph. Defaults to "".
        """
        timing, distances = remove_null_points(timing, distances)
        ax.scatter(timing, distances, s=12)
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Distance (mm)")

    def annotate_graph(self, ax: mpl.axes.Axes, timing: str, distance: int, description="") -> None:
        timing = datetime.datetime.strptime(timing, "%H:%M:%S")
        ax.annotate(description, xy=(timing, distance), xycoords="data", xytext=(timing, distance - 500), arrowprops=dict(arrowstyle="->"))
