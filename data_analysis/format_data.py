"""
Throughout this project, I collected data from the sensors through different
means, from which the data was stored in different formats. The idea of this
module is to reformat each set of data in a fixed structure. Distance
measurements by each sensor should be stored in a text file, each line
representing a point of measurement. Each line should be formatted as such:

TIME DISTANCE SIGNAL_STRENGTH

where, time, distance, and signal strength are values separated by a space.
"""

import os
import pathlib

import pandas as pd

os.chdir(os.path.realpath(os.path.dirname(__file__)))

TOF_INDOORS_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/indoors")
TOF_OUTDOORS_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/outdoors")
TOF_WITH_SHADE_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/with_shade")
LASER_INDOORS_RAW_DATA = pathlib.Path("./raw_data/laser_basic_tests/indoors")
LASER_OUTDOORS_RAW_DATA = pathlib.Path("./raw_data/laser_basic_tests/outdoors")

TOF_INDOORS_DATA = pathlib.Path("./data/tof_basic_tests/indoors")
TOF_OUTDOORS_DATA = pathlib.Path("./data/tof_basic_tests/outdoors")
TOF_WITH_SHADE_DATA = pathlib.Path("./data/tof_basic_tests/with_shade")
LASER_INDOORS_DATA = pathlib.Path("./data/laser_basic_tests/indoors")
LASER_OUTDOORS_DATA = pathlib.Path("./data/laser_basic_tests/outdoors")


def format_excel_data(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    """
    Format the excel data collected by the TOF software.

    Args:
        source_folder (pathlib.Path): Raw data's folder path.
        destination_folder (pathlib.Path): Formatted data's folder path.
    """
    for file_path in source_folder.iterdir():
        file_name = get_file_name(file_path)
        data = pd.read_excel(file_path)["distance(m)"]
        write_to_new_file(destination_folder, file_name, data)


def format_raspberry_pi_data(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    """
    Format the laser data collected by the Raspberry Pi.

    Args:
        source_folder (pathlib.Path): Raw data's folder path.
        destination_folder (pathlib.Path): Formatted data's folder path.
    """
    for file_path in source_folder.iterdir():
        file_name = get_file_name(file_path)
        data = get_raspberry_pi_data(file_path)
        write_to_new_file(destination_folder, file_name, data)


def format_laser_protocol_data(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    """
    Format the data collected by the laser's software.

    Args:
        source_folder (pathlib.Path): Raw data's folder path.
        destination_folder (pathlib.Path): Formatted data's folder path.
    """
    for file_path in source_folder.iterdir():
        file_name = get_file_name(file_path)
        data = get_laser_protocol_data(file_path)
        write_to_new_file(destination_folder, file_name, data)


def get_file_name(file_path: pathlib.Path) -> str:
    """
    Helper function to create a new file name for new data files based on the
    file names of the raw data file.s

    Args:
        file_path (pathlib.Path): Path to the raw data file.

    Returns:
        str: The file name without the file extension.
    """
    return file_path.name.split(".")[0]


def write_to_new_file(destination_folder: pathlib.Path, file_name: str, data: list[float]) -> None:
    """
    Write the formatted list of data to the new data file.

    Args:
        destination_folder (pathlib.Path): Formatted data's folder path.
        file_name (str): Formatted data's file name.
        data (list[float]): Formatted data to be written.
    """
    with open(destination_folder / f"{file_name}.txt", "w") as f:
        for distance in data:
            f.write(f"-1 {distance:.2f} -1\n")


def get_raspberry_pi_data(file_path: pathlib.Path) -> list[float]:
    """
    Helper function that formats a file of laser data collected by the
    Raspberry Pi.

    Args:
        file_path (pathlib.Path): Path to raw data file.

    Returns:
        list[float]: List of distance data.
    """
    data = []
    with open(file_path) as f:
        for line in f.readlines():
            _, distance, _ = line.rstrip().split(" ")
            distance = int(distance)
            if distance != -1:
                distance = round(distance / 1000, 2)
            data.append(distance)
    return data


def get_laser_protocol_data(file_path: pathlib.Path) -> list[float]:
    """
    Helper function that formats a file of laser data collected by the
    software.

    Args:
        file_path (pathlib.Path): Path to raw data file.

    Returns:
        list[float]: List of distance data.
    """
    data = []
    with open(file_path) as f:
        for line in f.readlines():
            protocol = line.split("]")[1].split(" ")
            distance_data = "".join(protocol[7:10])
            distance = round(int(distance_data, base=16) / 1000, 2)
            data.append(distance)
    return data


if __name__ == "__main__":
    format_excel_data(TOF_INDOORS_RAW_DATA, TOF_INDOORS_DATA)
    format_excel_data(TOF_OUTDOORS_RAW_DATA, TOF_OUTDOORS_DATA)
    format_raspberry_pi_data(TOF_WITH_SHADE_RAW_DATA, TOF_WITH_SHADE_DATA)
    format_laser_protocol_data(LASER_INDOORS_RAW_DATA, LASER_INDOORS_DATA)
    format_raspberry_pi_data(LASER_OUTDOORS_RAW_DATA, LASER_OUTDOORS_DATA)
