import matplotlib as mpl
import numpy as np

INTERVALS = [0.5 * i for i in range(1, 11)]


def plot_mean_vs_actual_distance(ax: mpl.axes.Axes, mean: list, title="") -> None:
    """
    Plot a line graph of the mean values at each distance interval. Also plot a line of
    the actual distances to compare to the TOF sensor's mean measurements.

    Args:
        ax (mpl.axes.Axes): Matplotlib axes object.
        mean (list): mean[i] is the mean of the data collected at the ith distance interval.
        title (str, optional): Title of graph. Defaults to "".
    """
    ax.plot(INTERVALS, mean)
    ax.plot(INTERVALS, INTERVALS, color="red", linestyle="--")
    _set_info(
        ax,
        title,
        "Actual Distance (m)",
        "Measured Mean (m)",
        legend=["TOF Sensor", "Actual Distance"],
    )


def plot_scatter(ax: mpl.axes.Axes, data: list[list], title="") -> None:
    """
    Plot a scatter plot of all the points measured by the sensor at each distance interval.

    Args:
        ax (mpl.axes.Axes): Matplotlib axes object.
        data (list[list]): data[i] is the list of points measured by the sensor at the ith
                            distance interval.
        title (str, optional): Title of graph. Defaults to "".
    """
    x, y = _flatten(data)
    ax.scatter(x, y, s=12, color="steelblue", alpha=0.2)
    _set_info(ax, title, "Actual Distance (m)", "Measured Points (m)")


def plot_std_errorbar(ax: mpl.axes.Axes, mean: list, std: list, title="") -> None:
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
    ax.errorbar(
        INTERVALS, mean, yerr=std, fmt="o", linestyle="", ecolor="red", capsize=2
    )
    _set_info(ax, title, "Actual Distance (m)", "Measured Points (m)")


def plot_best_fit_scatter(ax: mpl.axes.Axes, data: list[list], title="") -> None:
    """
    Given a scatter of all the points measured by the sensor, plot a best fit line.

    Args:
        ax (mpl.axes.Axes): Matplotlib axes object.
        data (list[list]): data[i] is the list of points measured by the sensor at the ith
                            distance interval.
        title (str, optional): Title of graph. Defaults to "".
    """
    x, y = _flatten(data)
    plot_scatter(ax, data, title=title)
    plot_line(ax, x, y)
    ax.plot(INTERVALS, INTERVALS, color="red", linestyle="--", label="y = x")
    ax.grid(color="#DEDEDE", linestyle="--", linewidth=1)
    ax.legend()


def plot_line(ax: mpl.axes.Axes, x: list, y: list) -> None:
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
    ax.set_xticks(INTERVALS)
    ax.set_yticks(INTERVALS)
    if legend:
        ax.legend(legend)


def _flatten(data: list[list]) -> tuple[list]:
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

    for i, interval in enumerate(INTERVALS):
        x.extend([interval] * len(data[i]))
        y.extend(data[i])

    return x, y
