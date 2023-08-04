import datetime
import pathlib


class FolderData:
    def __init__(self, folder_path: pathlib.Path) -> None:
        self.folder_path = folder_path
        self.data_loader = DataLoader()
        self.timings = []
        self.distances = []
        self.signal_strengths = []
        self.load_data()

    def load_data(self) -> None:
        self.timings, self.distances, self.signal_strengths = self.data_loader.load_data_from_folder(self.folder_path)


class DataLoader:
    def load_data_from_folder(self, folder_path: pathlib.Path) -> None:
        data = []
        for file_path in sorted(folder_path.iterdir()):
            timing, distance, signal_strength = self.load_data_from_file(file_path)
            data.append((timing, distance, signal_strength))
        return [list(i) for i in zip(*data)]

    def load_data_from_file(self, file_path: pathlib.Path, clean=True) -> list[float]:
        data = []
        with open(file_path) as f:
            for line in f.readlines():
                timing, distance, signal_strength = line.split(" ")
                timing = self.format_timing(timing)
                distance = float(distance)
                signal_strength = int(signal_strength)
                if clean and distance == -1:
                    continue
                data.append((timing, distance, signal_strength))
        return [list(i) for i in zip(*data)]

    def format_timing(self, timing: str) -> datetime.datetime:
        if timing == "-1":
            return "-1"
        return datetime.datetime.strptime(timing, "%H:%M:%S")
