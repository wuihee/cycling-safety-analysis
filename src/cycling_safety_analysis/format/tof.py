import pathlib

import pandas as pd

from . import utils


def format_excel(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    """
    Helper function to format data collected in excel files from WaveShare's default software.

    Args:
        source_folder (pathlib.Path): Raw data's folder path.
        destination_folder (pathlib.Path): Formatted data's folder path.
    """
    for file_path in source_folder.iterdir():
        file_name = utils.get_file_name(file_path)
        data = pd.read_excel(file_path)["distance(m)"]
        data = _pad_distance_data(data)
        utils.write_data_to_file(destination_folder, file_name, data)


def _pad_distance_data(data: list) -> list[tuple]:
    """
    Helper function to format the data correctly.

    Args:
        data (list): List of distance data extracted from the excel file.

    Returns:
        list[tuple]: Format it as (timing, distance, signal_strength)
    """
    new_data = []
    for distance in data:
        new_data.append((-1, distance, -1))
    return new_data
