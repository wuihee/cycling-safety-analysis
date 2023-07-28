import numpy as np


def get_mean_measurements(data: list[list[float]]) -> list[float]:
    """
    Get the mean of a list of data rounded to 2 decimal places.

    Args:
        data (list[list[float]]): A list containing a list of measured points for each interval.

    Returns:
        list[float]: Return an array containing the mean of the points at each interval.
    """
    return [round(np.mean(i), 2) for i in data]


def get_standard_deviations(data: list[list[float]]) -> list[float]:
    """
    Get the standard deviation of a list of data rounded to 2 decimal places.

    Args:
        data (list[list[float]]): A list containing a list of measured points for each interval.

    Returns:
        list[float]: Return an array containing the standard deviation of the points at each interval.
    """
    return [round(np.std(i), 2) for i in data]


def clean_array(data: list[float]) -> list[float]:
    """
    Given an array of data, remove all points 1 standard deviation from the mean.

    Args:
        data (list[float]): Data to be cleaned.

    Returns:
        list[float]: Returns array of cleaned points.
    """
    cleaned_array = []
    std = np.std(data)
    mean = np.mean(data)

    for measurement in data:
        if abs(measurement - mean) > std:
            continue
        cleaned_array.append(round(measurement, 2))

    return cleaned_array


def clean_tof_raw_data(raw_data: list[list[float]]) -> list[list[float]]:
    """
    Clean the measurements taken at each distance interval.

    Args:
        raw_data (list[list[float]]): data[i] is the distances measured at the ith interval.

    Returns:
        list[list[float]]: Return a list of clean measurements for each interval.
    """
    cleaned_data = []
    for measurements in raw_data:
        cleaned_data.append(clean_array(measurements))
    return cleaned_data


def remove_null_points(x: list, y: list, null_value=-1) -> tuple[list, list]:
    """
    Given the x and y values for a graph, remove all points where y = null_value.
    This is to prevent a whole row of -1 distances being plotted at the bottom of the graph.

    Args:
        x (list): x values to plot.
        y (list): y values to plot
        null_value (int, optional): The null value to be removed. Defaults to -1.

    Returns:
        tuple[list, list]: _description_
    """
    n = len(x)
    new_x = []
    new_y = []

    for i in range(n):
        if y[i] == null_value:
            continue
        new_x.append(x[i])
        new_y.append(y[i])

    return new_x, new_y


def clean_spurious_data(data: list[int]) -> list[int]:
    """
    Attempt to remove spurious data by removing standalone points.

    Args:
        data (list[int]): List of distances.

    Returns:
        list[int]: Cleaned list of distances.
    """
    cleaned_data = data.copy()

    for i, distance in enumerate(cleaned_data):
        if distance == -1:
            continue

        neighbors = get_neighbors(cleaned_data, i)
        if len(neighbors) <= 1:
            cleaned_data[i] = -1

    return cleaned_data


def get_neighbors(data: list[int], index: int, window=2) -> list[int]:
    """
    Get all non -1 neighbors of the point at index within left and right window.

    Args:
        data (list[int]): List of distances.
        index (int): Index of current point.
        window (int): Window to look for neighbors.

    Returns:
        list[int]: Non -1 neighbors.
    """
    neighbors = []

    for i in range(max(0, index - window), min(len(data), index + window + 1)):
        if data[i] != -1:
            neighbors.append(data[i])

    return neighbors
