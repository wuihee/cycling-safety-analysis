import datetime

import numpy as np


def get_mean(data: list) -> list[float]:
    """
    Get the mean of a list of data rounded to 2 decimal places.

    Args:
        data (list[list[float]]): A list containing a list of measured points for each interval.

    Returns:
        list[float]: Return an array containing the mean of the points at each interval.
    """
    return [round(np.mean(i), 2) for i in data]


def get_std(data: list) -> list[float]:
    """
    Get the standard deviation of a list of data rounded to 2 decimal places.

    Args:
        data (list[list[float]]): A list containing a list of measured points for each interval.

    Returns:
        list[float]: Return an array containing the standard deviation of the points at each interval.
    """
    return [round(np.std(i), 2) for i in data]


def datetime_to_timestamps(data: list[datetime.datetime]) -> list[int]:
    """
    Convert a list of datetime objects to integer representation.

    Args:
        data (list[datetime.datetime]): datetime data.

    Returns:
        list[int]: List of integers representing datetime objects.
    """
    return [int(dt.timestamp()) for dt in data]
