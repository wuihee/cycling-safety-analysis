import pathlib
from datetime import datetime

import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from data import analysis, processing


def scatter_time_vs_distance(
    ax: mpl.axes.Axes,
    x: list[datetime],
    y: list[int],
    title="",
    intervals=30,
    rotate_xticks=False,
    alpha=0.2,
    **kwargs,
) -> None:
    """
    Plot a time vs distance scatter graph.

    Args:
        ax (mpl.axes.Axes): Axes object to plot graph on.
        x (list[datetime]): x-values which are datetime objects.
        y (list[int]): y-values representing distances.
        title (str, optional): Title of graph. Defaults to "".
        intervals (int, optional): Time intervals between xticks. Defaults to
                                   30.
        rotate_xticks (bool, optional): Set to true to rotate xticks to make
                                        more space. Defaults to False.
    """
    x, y = _clean_null_values(x, y)
    ax.scatter(x, y, s=20, alpha=alpha, **kwargs)
    _set_info(ax, title)
    _set_xtick_intervals(ax, intervals)
    _format_xaxis(ax)
    if rotate_xticks:
        _rotate_xticks(ax)


def scatter_clusters_with_dbscan(
    ax: mpl.axes.Axes,
    x: list[datetime],
    y: list[int],
    title="",
    intervals=30,
    rotate_xticks=False,
) -> None:
    """
    Plot a scatter with circles drawn around clusters identified by DBSCAN.

    Args:
        ax (mpl.axes.Axes): Axes object to plot graph on.
        x (list[datetime]): x-values which are datetime objects.
        y (list[int]): y-values representing distances.
        title (str, optional): Title of graph. Defaults to "".
        intervals (int, optional): Time intervals between xticks. Defaults to
                                   30.
        rotate_xticks (bool, optional): Set to true to rotate xticks to make
                                        more space. Defaults to False.
    """
    x, y = _clean_null_values(x, y)
    timestamps = processing.datetime_to_timestamps(x)

    df = pd.DataFrame({"datetime": x, "distance": y, "timestamp": timestamps})
    clusters = analysis.find_clusters_DBSCAN(timestamps, y)
    df["clusters"] = clusters

    scatter_time_vs_distance(
        ax,
        x,
        y,
        title=title,
        intervals=intervals,
        rotate_xticks=rotate_xticks,
        c=clusters,
        edgecolors="k",
    )

    for cluster_id in [c for c in df["clusters"].unique() if c != -1]:
        cluster_data = df[df["clusters"] == cluster_id]
        centroid_x = cluster_data["datetime"].mean()
        centroid_y = cluster_data["distance"].mean()
        ax.plot(centroid_x, centroid_y, "bo", fillstyle="none", markersize=20)


def interactive_scatter(
    fig: mpl.figure.Figure,
    ax_1: mpl.axes.Axes,
    ax_2: mpl.axes.Axes,
    images: list[pathlib.Path],
    x: list[datetime],
    y: list[int],
    title="",
    **kwargs,
) -> None:
    """
    Plot an interactive scatter where the user can see each image associated
    with each point on the scatter.

    Args:
        fig (mpl.figure.Figure): Matplot
        ax_1 (mpl.axes.Axes): Axes to plot scatter.
        ax_2 (_type_): Axes to print image on.
        images (list[pathlib.Path]): List of image paths.
        x (list[datetime]): _description_
        y (list[int]): _description_
        title (str, optional): _description_. Defaults to "".
    """
    ax_1.scatter(x, y, picker=True, **kwargs)
    _set_info(ax_1, title, ylow=1000, yhigh=2500)
    _format_xaxis(ax_1)
    fig.canvas.mpl_connect("pick_event", lambda event: _on_pick(event, ax_2, images, y))
    ax_2.axis("off")


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


def _set_info(ax: mpl.axes.Axes, title: str, ylow=0, yhigh=5500, legend=None) -> None:
    """
    Set the information of a graph.

    Args:
        ax (mpl.Axes.axes): Matplotlib axes object.
        title (str): Title of graph.
        ylow (int): Lower bound of y-axis.
        yhigh (int): Upper bound of y-axis
        xticks (list): x axis tick values.
        yticks (list): y axis tick values.
        legend (list): Graph legend.
    """
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Distance (mm)")
    ax.set_yticks(range(ylow, yhigh, 500))
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
    """
    Rotate the xticks 45 degrees.

    Args:
        ax (mpl.axes.Axes): Matplotlib axes object.
    """
    ax.tick_params(axis="x", labelrotation=45)


def _on_pick(event, ax, images, distances):
    """
    Callback function for interactive plot.

    Args:
        event (_type_): _description_
        ax (_type_): _description_
        images (_type_): _description_
        distances (_type_): _description_
    """
    ax.clear()
    ax.axis("off")
    i = event.ind[0]
    img = np.asarray(Image.open(images[i]))
    ax.imshow(img)
    ax.text(
        0.5,
        0.5,
        f"Passing Distance: {distances[i] / 1000:.2f}m",
        color="white",
        fontsize=12,
        ha="center",
        va="center",
        bbox=dict(
            boxstyle="round,pad=0.3", facecolor="black", edgecolor="white", alpha=0.6
        ),
    )
    plt.draw()
