import numpy as np


def clean_spurious_data(data: list[int]) -> list[int]:
    """
    Attempt to remove spurious data by removing standalone points.

    Args:
        data (list[int]): List of distances.

    Returns:
        list[int]: Cleaned list of distances.
    """
    cleaned_data = data.copy()

    # Remove points greater than 2.5m.
    for i, distance in enumerate(cleaned_data):
        if distance >= 2500:
            cleaned_data[i] = -1

    # Points must be clustered together to be considered a pass.
    for i, distance in enumerate(cleaned_data):
        if distance == -1:
            continue

        neighbors = _get_neighbors(cleaned_data, i)
        if len(neighbors) <= 1:
            cleaned_data[i] = -1

    return cleaned_data


def clean_basic_test_data(data: list[list]) -> list[list]:
    """
    Clean the measurements taken at each distance interval.

    Args:
        data (list[list]): data[i] is the distances measured at the ith interval.

    Returns:
        list[list]: Return a list of clean measurements for each interval.
    """
    return [clean_std(measurements) for measurements in data]


def clean_std(data: list) -> list:
    """
    Given an array of data, remove all points std standard deviations from the mean.

    Args:
        data (list): Array of data.

    Returns:
        list: Cleaned array.
    """
    cleaned_array = []
    std = np.std(data)
    mean = np.mean(data)

    for measurement in data:
        if abs(measurement - mean) > std:
            continue
        cleaned_array.append(round(measurement, 2))

    return cleaned_array


def fliter_above(data: list[int], threshold: int) -> list[int]:
    """
    Filter all points above the given threshold.

    Args:
        data (list[int]): List of distances.
        threshold (int): Threshold to filter.

    Returns:
        list[int]: Distance data but all points above threshold now -1.
    """
    return [i if i < threshold else -1 for i in data]


def _get_neighbors(data: list[int], index: int, window=2) -> list[int]:
    """
    Get all non -1 neighbors of the point at index within left and right window.

    Args:
        data (list[int]): List of distances.
        index (int): Index of current point.
        window (int): Window to look for neighbors.

    Returns:
        list[int]: Indices of the non -1 neighbors.
    """
    neighbors = []

    for i in range(max(0, index - window), min(len(data), index + window + 1)):
        if data[i] != -1:
            neighbors.append(i)

    return neighbors
