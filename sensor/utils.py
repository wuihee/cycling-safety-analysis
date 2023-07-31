import os


def cd_to_parent_dir() -> None:
    """
    Change the working directory to that of the parent directory.
    """
    os.chdir(os.path.dirname(os.path.realpath(__file__)))


def write_to_file(path: str, message: str, mode="a") -> None:
    """
    Utility function to write message to file.

    Args:
        (str) path: Path to file.
        (str) message: Message to write.
        (str) mode: Mode of writing to file. Default is append.
    """
    with open(path, mode) as file:
        file.write(message + "\n")
