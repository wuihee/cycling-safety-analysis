from sensor import Sensor


class TOFSensor(Sensor):
    def __init__(self) -> None:
        super().__init__("/dev/ttyS0", 921600)

    def get_data(self) -> str:
        """
        Get data in a consistent format to be published to MQTT.

        Returns:
            str: Formatted data consisting of the time, distance and signal strength.
        """
        distance, signal_strength = self.measure_distance()
        return f"{self.current_time} {distance} {signal_strength}"

    def measure_distance(self) -> tuple[int, int]:
        """
        Measure the current distance with the laser sensor.

        Returns:
            tuple[int, int]: distance and signal strength respectively.
        """
        protocol = self._read_distance_protocol()
        if not self._is_valid_protocol(protocol):
            return -1, -1

        distance = self._get_distance_from_protocol(protocol)
        strength = self._get_strength_from_protocol(protocol)
        if strength == 0:
            distance = -1
        return distance, strength

    def _read_distance_protocol(self) -> list[int]:
        """
        Read the protocol created by measuring distance, which is 13 bytes long.

        Returns:
            list[int]: An array of decimals reprenting the resepective bytes.
        """
        return self._read_protocol(16)

    def _is_valid_protocol(self, protocol: list[int]) -> bool:
        """
        Determine if the protocol is valid.

        Args:
            protocol (list[int]): The protocol of data from the sensor.

        Returns:
            bool: True if protocol is valid else false.
        """
        if not protocol:
            return None
        return sum(protocol[:-1]) % 256 == protocol[-1]

    def _get_distance_from_protocol(self, protocol: str) -> int:
        """
        Find the distance measured given a distance protocol. The distance
        is found by representing bytes 8 to 10 (0-based indexing), converting
        them to hex and finding the integer representation.

        Args:
            protocol (str): Distance protocol from self._read_distance_prtocol().

        Returns:
            int: Distance in mm.
        """
        return self._get_value_from_protocol(protocol, 8, 10)

    def _get_strength_from_protocol(self, protocol: str) -> int:
        """
        Find the signal strength from a given distance protocol. The signal
        strength is found by converting bytes 12 and 13 (0-based indexing)
        to hex and finding the integer representation.

        Args:
            protocol (str): Distance protocol from self._read_distance_prtocol().

        Returns:
            int: The higher the signal strength the more inaccurate the distance.
        """
        return self._get_value_from_protocol(protocol, 12, 13)


if __name__ == "__main__":
    sensor = TOFSensor()
    print(sensor.get_data())
