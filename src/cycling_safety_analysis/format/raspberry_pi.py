import pathlib

from . import utils


def format_text(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    """
    Format the laser data collected by the Raspberry Pi.

    Args:
        source_folder (pathlib.Path): Raw data's folder path.
        destination_folder (pathlib.Path): Formatted data's folder path.
    """
    for file_path in source_folder.iterdir():
        file_name = utils.get_file_name(file_path)
        data = _get_text_data(file_path)
        utils.write_data_to_file(destination_folder, file_name, data)


def _get_text_data(file_path: pathlib.Path) -> list[float]:
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
            distance = float(distance)
            if distance != -1:
                distance = round(distance / 1000, 2)
            data.append((-1, distance, -1))
    return data
