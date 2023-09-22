import pathlib


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


def write_data_to_file(destination_folder: pathlib.Path, file_name: str, data: list[float]) -> None:
    """
    Write the formatted list of data to the new data file.

    Args:
        destination_folder (pathlib.Path): Formatted data's folder path.
        file_name (str): Formatted data's file name.
        data (list[float]): Formatted data to be written.
    """
    with open(destination_folder / f"{file_name}.txt", "w") as f:
        for timing, distance, strength in data:
            f.write(f"{timing} {distance:.2f} {strength}\n")
