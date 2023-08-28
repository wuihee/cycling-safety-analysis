from datetime import datetime

import matplotlib as mpl
import matplotlib.dates as mdates


def scatter_time_vs_distance(
    ax: mpl.axes.Axes,
    x: list[datetime],
    y: list[int],
    title="",
    intervals=30,
    rotate_xticks=False,
) -> None:
    x, y = _clean_null_values(x, y)
    ax.scatter(x, y, s=20, alpha=0.2)
    _set_info(ax, title, "Time", "Distance (mm)")
    _set_xtick_intervals(ax, intervals)
    _format_xaxis(ax)
    if rotate_xticks:
        _rotate_xticks(ax)


def _clean_null_values(x: list, y: list, null_value=-1) -> tuple[int]:
    """
    Return the data containing all points that are not null. Used to plot a
    cleaner scatter graph.

    Args:
        x (list): datetime values on the x-axis.
        y (list): distance values on the y-axis.
        null_value (int, optional): The null value to clean. Defaults to -1.

    Returns:
        tuple[int]: x, y values to plot.
    """
    non_null_indices = [i for i in range(len(y)) if y[i] != null_value]
    x = [x[i] for i in non_null_indices]
    y = [y[i] for i in non_null_indices]
    return x, y


def _set_info(
    ax: mpl.axes.Axes, title: str, xlabel: str, ylabel: str, legend=None
) -> None:
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


def _set_xtick_intervals(ax: mpl.axes.Axes, intervals: int) -> None:
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=intervals))


def _format_xaxis(ax: mpl.axes.Axes) -> None:
    """
    Format the x-axis to display time in HH:MM:SS with intervals of 30s.

    Args:
        ax (mpl.axes.Axes): Matplotlib axes object.
        intervals (int, optional): The number of seconds between xticks.
                                   Defaults to 30.
    """
    time_format = mdates.DateFormatter("%H:%M:%S")
    ax.xaxis.set_major_formatter(time_format)


def _rotate_xticks(ax: mpl.axes.Axes) -> None:
    ax.tick_params(axis="x", labelrotation=45)
