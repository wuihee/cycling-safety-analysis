import os
import pathlib

import pandas as pd

os.chdir(os.path.realpath(os.path.dirname(__file__)))

TOF_INDOORS_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/indoors")
TOF_OUTDOORS_RAW_DATA = pathlib.Path("./raw_data/tof_basic_tests/outdoors")
LASER_INDOORS_RAW_DATA = pathlib.Path("./raw_data/laser_basic_tests/indoors")
LASER_OUTDOORS_RAW_DATA = pathlib.Path("./raw_data/laser_basic_tests/outdoors")

TOF_INDOORS_DATA = pathlib.Path("./data/tof_basic_tests/indoors")
TOF_OUTDOORS_DATA = pathlib.Path("./data/tof_basic_tests/outdoors")
LASER_INDOORS_DATA = pathlib.Path("./data/laser_basic_tests/indoors")
LASER_OUTDOORS_DATA = pathlib.Path("./data/laser_basic_tests/outdoors")


def format_excel_data(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    for file_path in source_folder.iterdir():
        file_name = file_path.name.split(".")[0]
        data = pd.read_excel(file_path)["distance(m)"]
        with open(destination_folder / f"{file_name}.txt", "w") as f:
            for distance in data:
                f.write(f"-1 {distance:.2f} -1\n")


def format_laser_txt_data(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    for file_path in source_folder.iterdir():
        file_name = file_path.name.split(".")[0]
        data = []
        with open(file_path) as f:
            for line in f.readlines():
                _, distance, _ = line.rstrip().split(" ")
                distance = round(int(distance) / 1000, 2)
                data.append(distance)
        with open(destination_folder / f"{file_name}.txt", "w") as f:
            for distance in data:
                f.write(f"-1 {distance:.2f} -1\n")


if __name__ == "__main__":
    format_excel_data(TOF_INDOORS_RAW_DATA, TOF_INDOORS_DATA)
    format_excel_data(TOF_OUTDOORS_RAW_DATA, TOF_OUTDOORS_DATA)
    format_laser_txt_data(LASER_OUTDOORS_RAW_DATA, LASER_OUTDOORS_DATA)
