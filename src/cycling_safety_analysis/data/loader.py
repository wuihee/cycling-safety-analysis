import datetime
import pathlib

from . import cleaner


class FolderData:
    def __init__(self, folder_path: pathlib.Path) -> None:
        """
        Initialize attributes to store data from folder.

        Args:
            folder_path (pathlib.Path): Path to folder to load data from.
        """
        self.folder_path = folder_path
        self.timings = []
        self.distances = []
        self.signal_strengths = []
        self.load_data()

    def load_data(self) -> None:
        """
        Load data from each files into the respective attributes.
        """
        self.timings, self.distances, self.signal_strengths = load_data_from_folder(
            self.folder_path
        )


def load_data_from_folder(folder_path: pathlib.Path) -> list[list[list]]:
    """
    Extract the data from each file in the folder.

    Args:
        folder_path (pathlib.Path): Path to folder.

    Returns:
        list[list[list]]: A list containing the data of each file.
    """
    data = []

    for file_path in sorted(folder_path.iterdir()):
        timing, distance, signal_strength = load_data_from_file(file_path)
        data.append((timing, distance, signal_strength))

    return [list(i) for i in zip(*data)]


def filter_data_from_file(file_path: pathlib.Path, high=3500, low=0) -> tuple[list]:
    """
    Helper function that extracts data from file.

    Args:
        file_path (pathlib.Path): Data file.

    Returns:
        tuple[list]: Returns timings, distances, and signal strengths.
    """
    timings, distances, strengths = load_data_from_file(file_path)
    distances = cleaner.filter(distances, high, low)
    return timings, distances, strengths


def load_data_from_file(file_path: pathlib.Path, clean=True) -> list[list]:
    """
    Given a file that stores data from the sensor in a standard format
    speicified in format_data.py, extract the distances, timings, and
    signal strengths.

    Args:
        file_path (pathlib.Path): Path to file.
        clean (bool, optional): If true, remove points with invalid
                                distance measurements. Defaults to True.

    Returns:
        list[list]: Returns three lists: timings, distances, and signal
                    strengths respectively.
    """
    data = []

    with open(file_path) as f:
        for line in f.readlines():
            timing, distance, signal_strength = line.split(" ")
            timing = _format_timing(timing)
            distance = float(distance)
            signal_strength = int(signal_strength)

            if clean and distance == -1:
                continue

            data.append((timing, distance, signal_strength))

    return [list(i) for i in zip(*data)]


def _format_timing(timing: str) -> datetime.datetime:
    if timing == "-1":
        return "-1"
    dt = datetime.datetime.strptime(timing, "%H:%M:%S")
    dt.replace(year=2023)
    return dt
