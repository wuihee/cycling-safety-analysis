import numpy as np


def get_mean_measurements(data: list) -> list[float]:
    """
    Get the mean of a list of data rounded to 2 decimal places.

    Args:
        data (list[list[float]]): A list containing a list of measured points for each interval.

    Returns:
        list[float]: Return an array containing the mean of the points at each interval.
    """
    return [round(np.mean(i), 2) for i in data]


def get_standard_deviations(data: list) -> list[float]:
    """
    Get the standard deviation of a list of data rounded to 2 decimal places.

    Args:
        data (list[list[float]]): A list containing a list of measured points for each interval.

    Returns:
        list[float]: Return an array containing the standard deviation of the points at each interval.
    """
    return [round(np.std(i), 2) for i in data]
