import numpy as np


def clean_tof_data(data: list[int]) -> list[int]:
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


def clean_laser_data(data: list[int]) -> list:
    cleaned_data = data.copy()

    # Merge clusters which are within 2 seconds of each other.

    # Average the values of clusters.
    cleaned_data = average_clusters(cleaned_data)

    return cleaned_data


def average_clusters(distances: list) -> list:
    """
    Given a list of distance measurements, a cluster is a contiguous subarray
    of non-null points. Average the values of all clusters.

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
