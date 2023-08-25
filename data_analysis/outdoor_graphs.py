import datetime

import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np


def scatter_time_vs_distance(
    ax: mpl.axes.Axes, timings: list[datetime.datetime], distances: list[int], title=""
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
    non_null_indices = _get_non_null_indices(distances)
    x = _clean_null_values(timings, non_null_indices)
    y = _clean_null_values(distances, non_null_indices)
    _plot_scatter(ax, x, y, title)


def scatter_average_clusters(
    ax: mpl.axes.Axes, timings: list[datetime.datetime], distances: list[int], title=""
) -> None:
    non_null_indices = _get_non_null_indices(distances)
    x = _clean_null_values(timings, non_null_indices)
    y = _clean_null_values(_average_clusters(distances), non_null_indices)
    _plot_scatter(ax, x, y, title)


def _plot_scatter(ax: mpl.axes.Axes, x: list, y: list, title) -> None:
    """
    Helper function to plot a scatter graph.

    Args:
        ax (mpl.axes.Axes): Matplotlib axes object.
        x (list): x values.
        y (list): y values.
        title (str, optional): Title of the graph.
    """
    ax.scatter(x, y, s=20, alpha=0.2)
    _set_info(ax, title, "Time", "Distance (mm)")
    _format_time_xaxis(ax)


def _set_info(ax: mpl.axes.Axes, title: str, xlabel: str, ylabel: str, legend=None) -> None:
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


def _format_time_xaxis(ax: mpl.axes.Axes) -> None:
    """
    Format the x-axis to display time in HH:MM:SS with intervals of 30s.

    Args:
        ax (mpl.axes.Axes): Matplotlib axes object.
    """
    time_format = mdates.DateFormatter("%H:%M:%S")
    ax.xaxis.set_major_formatter(time_format)
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))


def _average_clusters(distances: list) -> list:
    """
    Average the values of all clusters and return the list.

    Args:
        distances (list): List of distance measurements by the sensor.

    Returns:
        list: A list of equal length with the distance of clusters averaged.
    """
    new_distances = distances.copy()
    i = 0

    # Loop through distances.
    while i < len(distances):
        # If cluster is encountered, iterate until the end of the cluster.
        if distances[i] != -1:
            j = i
            while j < len(distances) - 1 and distances[j] != -1:
                j += 1

            # Find the mean of the cluster.
            mean = np.mean([distances[k] for k in range(i, j)])

            # Replace values in the cluster with the mean.
            for k in range(i, j):
                new_distances[k] = mean

            # Move pointer i to the end of the cluster.
            i = j

        i += 1

    return new_distances


def _clean_null_values(data: list[int], non_null_indices: list[int]) -> list[int]:
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


def _get_non_null_indices(data: list[int], null_value=-1) -> list[int]:
    """
    Return a list indices in data representing the non null values.

    Args:
        data (list[int]): Data array to be searched.
        null_value (int, optional): The null value to check for. Defaults to -1.

    Returns:
        list[int]: List of indices.
    """
    return [i for i in range(len(data)) if data[i] != null_value]
