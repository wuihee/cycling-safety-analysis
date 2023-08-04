import pathlib


class LoadFolder:
    """
    I want to load the distances measured by the sensors from each basic test folder.
    """

    def __init__(self, folder_path: pathlib.Path) -> None:
        self.folder_path = folder_path

    def get_distance_data(self) -> list[float]:
        data = []
        for file_path in self.folder_path.iterdir():
            distance_interval = []
            with open(file_path) as f:
                for line in f.readlines():
                    _, distance, _ = line.split(" ")
                    distance = float(distance)
                    distance_interval.append(distance)
            data.append(self.clean_invalid_points(distance_interval))
        return data

    def clean_invalid_points(self, data: list[float]) -> list[float]:
        return [measurement for measurement in data if measurement != -1]
