import pathlib

from . import utils


def format_protocol_data(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    """
    Format hex data collected by the laser's software.

    Args:
        source_folder (pathlib.Path): Raw data's folder path.
        destination_folder (pathlib.Path): Formatted data's folder path.
    """
    for file_path in source_folder.iterdir():
        file_name = utils.get_file_name(file_path)
        data = _get_protocol_data(file_path)
        utils.write_data_to_file(destination_folder, file_name, data)


def format_ascii_data(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    """
    Format ASCII data collected by the laser's software.

    Args:
        source_folder (pathlib.Path): Raw data's folder path.
        destination_folder (pathlib.Path): Formatted data's folder path.
    """
    for file_path in source_folder.iterdir():
        file_name = utils.get_file_name(file_path)
        data = _get_ascii_data(file_path)
        utils.write_data_to_file(destination_folder, file_name, data)


def _get_protocol_data(file_path: pathlib.Path) -> list[float]:
    """
    Helper function that formats a file of laser hex data collected by
    the software.

    Args:
        file_path (pathlib.Path): Path to raw data file.

    Returns:
        list[float]: List of distance data.
    """
    data = []
    with open(file_path) as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                protocol = _extract_protocol(line)
                distance = _extract_distance_from_protocol(protocol)
                data.append((-1, distance, -1))
    return data


def _get_ascii_data(file_path: pathlib.Path) -> list[float]:
    """
    Helper function that formats a file of laser ASCII data collected
    by the software.

    Args:
        file_path (pathlib.Path): Path to raw data file.

    Returns:
        list[float]: List of distance data.
    """
    data = []
    with open(file_path) as f:
        for line in f.readlines():
            line = line.strip()
            if _is_valid_line(line):
                timing = _extract_time(line)
                distance = _extract_ascii(line)
                data.append((timing, float(distance), -1))
    return data


def _is_valid_line(line: str) -> bool:
    """
    Return if the line is in a valid format. Currently the test is a little
    simplistic. I will improve on it if needed.

    Args:
        line (str): The line of data recorded by the laser software.

    Returns:
        bool: True if the line is in a standard format containing useful data.
    """
    return "]" in line


def _extract_time(line: str) -> str:
    """
    Extract the time from a line of raw data.

    Args:
        line (str): Line of raw data from the laser software.

    Returns:
        str: The time in HH:MM:SS.
    """
    return line.split(" ")[1].split(".")[0]


def _extract_protocol(line: str) -> list[str]:
    """
    Extract the protocol from a line of raw data.

    Args:
        line (str): Line of raw data from the laser software.

    Returns:
        list[str]: Protocol in [byte1, byte2, etc...].
    """
    return line.split("]")[1].split(" ")


def _extract_distance_from_protocol(protocol: list[str]) -> str:
    """
    Given a protocol of bytes, extract the distance from it.

    Args:
        protocol (list[str]): Protocol in [byte1, byte2, etc...].

    Returns:
        str: The distance in m.
    """
    distance_data = "".join(protocol[7:10])
    return round(int(distance_data, base=16) / 1000, 2)


def _extract_ascii(line: str) -> int:
    """
    Extract the ASCII distance from a line of raw data.

    Args:
        line (str): Line of raw data from the laser software.

    Returns:
        str: Distance in m.
    """
    distance = line.split("]")[1]
    if _is_valid_distance(distance):
        return int(distance)
    return -1


def _is_valid_distance(distance: str) -> bool:
    return all(character.isdigit() for character in distance)
