import datetime

import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np


class BasicGraphs:
    def __init__(self) -> None:
        self.intervals = [0.5 * i for i in range(1, 11)]

    def plot_mean_vs_actual_distance(self, ax: mpl.axes.Axes, mean: list, title="") -> None:
        """
        Plot a line graph of the mean values at each distance interval. Also plot a line of
        the actual distances to compare to the TOF sensor's mean measurements.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
            mean (list): mean[i] is the mean of the data collected at the ith distance interval.
            title (str, optional): Title of graph. Defaults to "".
        """
        ax.plot(self.intervals, mean)
        ax.plot(self.intervals, self.intervals, color="red", linestyle="--")
        self._set_info(ax, title, "Actual Distance (m)", "Measured Mean (m)", legend=["TOF Sensor", "Actual Distance"])

    def plot_scatter(self, ax: mpl.axes.Axes, data: list[list], title="") -> None:
        """
        Plot a scatter plot of all the points measured by the sensor at each distance interval.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
            data (list[list]): data[i] is the list of points measured by the sensor at the ith
                               distance interval.
            title (str, optional): Title of graph. Defaults to "".
        """
        x, y = self._flatten(data)
        ax.scatter(x, y, s=12, color="steelblue")
        self._set_info(ax, title, "Actual Distance (m)", "Measured Points (m)")

    def plot_std_errorbar(self, ax: mpl.axes.Axes, mean: list, std: list, title="") -> None:
        """
        Plot the mean measurements at each distance interval, and the errorbars showing the
        respective standard deviation at each interval.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
            mean (list): mean[i] is the mean of the data collected at the ith distance interval.
            std (list): std[i] is the standard deviation of the points collected by the sensor
                        at the ith distance interval.
            title (str, optional): Title of graph. Defaults to "".
        """
        ax.errorbar(self.intervals, mean, yerr=std, fmt="o", linestyle="", ecolor="red", capsize=2)
        self._set_info(ax, title, "Actual Distance (m)", "Measured Points (m)")

    def plot_best_fit_scatter(self, ax: mpl.axes.Axes, data: list[list], title="") -> None:
        """
        Given a scatter of all the points measured by the sensor, plot a best fit line.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
            data (list[list]): data[i] is the list of points measured by the sensor at the ith
                               distance interval.
            title (str, optional): Title of graph. Defaults to "".
        """
        x, y = self._flatten(data)
        self.plot_scatter(ax, data, title=title)
        self.plot_line(ax, x, y)
        ax.plot(self.intervals, self.intervals, color="red", linestyle="--", label="y = x")
        ax.grid(color="#DEDEDE", linestyle="--", linewidth=1)
        ax.legend()

    def plot_line(self, ax: mpl.axes.Axes, x: list, y: list) -> None:
        """
        Given a list of x and y coordinates, plot a best fit line.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
            x (list): x points.
            y (list): y points.
        """
        m, b = np.polyfit(x, y, deg=1)
        best_fit = np.poly1d((m, b))
        equation = f"y = {m:.2f}x + {b:.2f}"
        ax.plot(x, best_fit(x), color="green", linestyle="--", label=equation)

    def _set_info(self, ax: mpl.axes.Axes, title: str, xlabel: str, ylabel: str, legend=None) -> None:
        """
        Set the information of a graph.

        Args:
            ax (mpl.Axes.axes): Matplotlib axes object.
            title (str): Title of graph.
            xlabel (str): Title of x label.
            ylabel (str): Title of y label.
            xticks (list): x axis tick values.
            yticks (list): y axis tick values.
            legend (list): Graph legend.
        """
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(self.intervals)
        ax.set_yticks(self.intervals)
        if legend:
            ax.legend(legend)

    def _flatten(self, data: list[list]) -> tuple[list]:
        """
        Return a list of x and y points of TOF sensor measurements and respective distant
        intervals.

        Args:
            data (list[list]): data[i] is the list of points measured by the sensor at the ith
                               distance interval.

        Returns:
            tuple[list]]: measurements x, and respective distant intervals y.
        """

        x, y = [], []

        for i, interval in enumerate(self.intervals):
            x.extend([interval] * len(data[i]))
            y.extend(data[i])

        return x, y


class OutdoorGraphs:
    def scatter_time_vs_distance(
        self, ax: mpl.axes.Axes, timings: list[datetime.datetime], distances: list[int], title=""
    ) -> None:
        """
        Plot a scatter plot of time against distance.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
            timings (list[datetime.datetime]): List of timings for each distance measured.
            distances (list[int]): List of distances measured by the sensor.
            title (str, optional): Title of the graph. Defaults to "".
        """
        # Clean the null values from the distances data.
        non_null_indices = self._get_non_null_indices(distances)
        x = self._clean_null_values(timings, non_null_indices)
        y = self._clean_null_values(distances, non_null_indices)

        ax.scatter(x, y, s=20, alpha=0.2)
        self._set_info(ax, title, "Time", "Distance (mm)")
        self._format_time_xaxis(ax)

    def scatter_average_clusters(
        self, ax: mpl.axes.Axes, timings: list[datetime.datetime], distances: list[int], title=""
    ) -> None:
        non_null_indices = self._get_non_null_indices(distances)
        x = self._clean_null_values(timings, non_null_indices)
        y = self._clean_null_values(self._get_average_clusters(distances), non_null_indices)

        ax.scatter(x, y, s=20, alpha=0.2)
        self._set_info(ax, title, "Time", "Distance (mm)")
        self._format_time_xaxis(ax)

    def _get_average_clusters(ax, distances):
        new_distances = distances.copy()
        i = 0
        while i < len(distances):
            if distances[i] != -1:
                j = i
                while distances[j] != -1:
                    j += 1
                mean = np.mean([distances[k] for k in range(i, j)])
                for k in range(i, j):
                    new_distances[k] = mean
                i = j
            i += 1
        return new_distances

    def _set_info(self, ax: mpl.axes.Axes, title: str, xlabel: str, ylabel: str, legend=None) -> None:
        """
        Set the information of a graph.

        Args:
            ax (mpl.Axes.axes): Matplotlib axes object.
            title (str): Title of graph.
            xlabel (str): Title of x label.
            ylabel (str): Title of y label.
            xticks (list): x axis tick values.
            yticks (list): y axis tick values.
            legend (list): Graph legend.
        """
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_yticks(range(0, 5500, 500))
        ax.grid(color="#DEDEDE", linestyle="--", linewidth=1)
        if legend:
            ax.legend(legend)

    def _format_time_xaxis(self, ax: mpl.axes.Axes) -> None:
        """
        Format the x-axis to display time in HH:MM:SS with intervals of 30s.

        Args:
            ax (mpl.axes.Axes): Matplotlib axes object.
        """
        time_format = mdates.DateFormatter("%H:%M:%S")
        ax.xaxis.set_major_formatter(time_format)
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))

    def _get_non_null_indices(self, data: list[int], null_value=-1) -> list[int]:
        """
        Return a list indices in data representing the non null values.

        Args:
            data (list[int]): Data array to be searched.
            null_value (int, optional): The null value to check for. Defaults to -1.

        Returns:
            list[int]: List of indices.
        """
        return [i for i in range(len(data)) if data[i] != null_value]

    def _clean_null_values(self, data: list[int], non_null_indices: list[int]) -> list[int]:
        """
        Return the data containing all points that are not null. Used to plot a cleaner
        scatter graph.

        Args:
            data (list[int]): Data array to be searched.
            non_null_indices (list[int]): non_null_indices[i] indicates that the data[i] is
                                          non null.

        Returns:
            list[int]: New data which has no null values.
        """
        return [data[i] for i in non_null_indices]

    def _convert_to_datetime(self, timing: str) -> datetime.datetime:
        """
        Convert string to datetime object.

        Args:
            timing (str): Format of string is HH:MM:SS.

        Returns:
            datetime.datetime: String as a datetime object.
        """
        return datetime.datetime.strptime(timing, "%H:%M:%S")
