import pathlib


class LoadFolder:
    """
    I want to load the distances measured by the sensors from each basic test folder.
    """

    def __init__(self, folder_path: pathlib.Path) -> None:
        self.folder_path = folder_path

    def get_distance_from_folder(self) -> list[float]:
        data = []
        for file_path in sorted(self.folder_path.iterdir()):
            distance_interval = self.get_distance_from_file(file_path)
            data.append(self.clean_invalid_points(distance_interval))
        return data

    def get_distance_from_file(self, file_path) -> list[float]:
        data = []
        with open(file_path) as f:
            for line in f.readlines():
                _, distance, _ = line.split(" ")
                distance = float(distance)
                data.append(distance)
        return data

    def clean_invalid_points(self, data: list[float]) -> list[float]:
        return [measurement for measurement in data if measurement != -1]
