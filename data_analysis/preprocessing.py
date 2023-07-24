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
