import os
import pathlib

import pandas as pd

os.chdir(os.path.realpath(os.path.dirname(__file__)))

raw_folder_path = pathlib.Path("./raw_data/tof_basic_tests/indoors")
data_folder_path = pathlib.Path("./data/tof_basic_tests/indoors")

for file_path in raw_folder_path.iterdir():
    file_name = file_path.name.split(".")[0]
    data = pd.read_excel(file_path)["distance(m)"]
    file_path = data_folder_path / f"{file_name}.txt"

    with open(file_path, "w") as file:
        for distance in data:
            file.write(f"-1 {distance} -1\n")
