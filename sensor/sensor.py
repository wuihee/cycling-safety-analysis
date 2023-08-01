import datetime

import serial


class Sensor:
    def __init__(self, port: str, baudrate: int) -> None:
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)

    @property
    def current_time(self) -> str:
        """
        Returns the current time.

        Returns:
            str: Format is HH:MM:SS
        """
        t = str(datetime.datetime.now())
        return t.split(" ")[1].split(".")[0]

    def _read_protocol(self, number_of_bytes: int) -> list[int]:
        """
        Read a specified number of bytes from the sensor which forms a protocol.

        Args:
            number_of_bytes (int): Number of bytes to read from the sensor.

        Returns:
            list[int]: An array of bytes expressed in decimal.
        """
        return [byte for byte in self.ser.read(number_of_bytes)]

    def _get_value_from_protocol(self, protocol: list[int], start: int, end: int) -> int:
        """
        Get a speicifed value from the protocol, e.g. distance, signal strength.

        Args:
            protocol (list[int]): Protocol from self._read_protocol().
            start (int): The start index of the information.
            end (int): The end index of the information.

        Returns:
            int: The value of the information requested.
        """
        information = protocol[start : end + 1]
        return int(self._to_hex_string(information), base=16)

    def _to_hex_string(self, information: list[int]) -> str:
        """
        Takes a slice of the bytes in protocol and converts it into a single hex string.

        Args:
            information (list[int]): List of decimal bytes.

        Returns:
            str: Hexadecimal string representing the information bytes.
        """
        return "".join(self._to_hex(byte) for byte in information)

    def _to_hex(self, byte: int) -> str:
        """
        Converts a decimal byte to a hexamdecimal.

        Args:
            byte (int): Byte in decimal.

        Returns:
            str: Hexamdecimal byte of length.
        """
        return hex(byte)[2:].zfill(2)
