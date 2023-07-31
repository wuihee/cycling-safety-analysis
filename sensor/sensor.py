import datetime

import serial

# 921600 is SUPER important.
ser = serial.Serial("/dev/ttyS0", 921600)
ser.reset_input_buffer()


class Sensor:
    def __init__(self) -> None:
        self.TOF_HEADER = 87, 0, 255
        self.TOF_LENGTH = 16

    @property
    def current_time(self) -> str:
        """
        Return the current time.

        Returns:
            str: Format is HH:MM:SS.
        """
        t = str(datetime.datetime.now())
        return t.split(" ")[1].split(".")[0]

    def get_data(self) -> str:
        """
        Returns time and distance measured by the TOF sensor currently.

        Returns:
            str: Returns a string containing the time, distance, and signal strength.
        """
        if ser.in_waiting < 16:
            return ""

        protocol = self.get_protocol()
        if not self.is_valid_protocol(protocol):
            return "Invalid Protocol"

        signal_strength = self.get_signal_strength(protocol)
        if signal_strength == 0:
            data = f"{self.current_time} -1 0"
        else:
            distance = self.get_distance(protocol)
            data = f"{self.current_time} {distance} {signal_strength}"

        return data

    def get_protocol(self) -> tuple[int]:
        """
        Reads from serial and retrieves the TOF protocol.

        Returns:
            tuple[int]: Protocol includes: Frame Header + Function Mark + Data + Sum Check
        """
        protocol = ()
        for _ in range(0, 16):
            protocol += (ord(ser.read(1)),)
        return protocol

    def is_valid_protocol(self, protocol: tuple[int]) -> bool:
        """
        Verify the entire protocol.

        Returns:
            bool: Return true if the protocol is valid else false.
        """
        if self.is_valid_header(protocol) and self.is_valid_checksum(protocol):
            return True
        return False

    def is_valid_header(self, protocol: tuple[int]) -> bool:
        """
        Verify the protocol header.

        Returns:
            bool: Returns true if the header is valid else false.
        """
        if protocol[:3] == self.TOF_HEADER:
            return True
        return False

    def is_valid_checksum(self, protocol: tuple[int]) -> bool:
        """
        Verify the protocol checksum.

        Returns:
            bool: Returns true if the checksum is valid else false.
        """
        if len(protocol) < self.TOF_LENGTH:
            return False

        TOF_check = sum(protocol[i] for i in range(self.TOF_LENGTH - 1)) % 256
        if TOF_check == protocol[self.TOF_LENGTH - 1]:
            return True
        return False

    def get_signal_strength(self, protocol: tuple[int]) -> int:
        """
        Get the signal strength of the current measurement.

        Args:
            (tuple[int]) protocol: The current TOF protocol data.

        Returns:
            int: Returns an integer indicating signal strength.
        """
        return (protocol[12]) | (protocol[13] << 8)

    def get_distance(self, protocol: tuple[int]) -> int:
        """
        Get the distance measured by the sensor.

        Args:
            (tuple[int]) protocol: The current TOF protocol data.

        Returns:
            int: Returns an integer indicating the distance (mm).
        """
        return protocol[8] | (protocol[9] << 8) | (protocol[10] << 16)


if __name__ == "__main__":
    print("sensor module to be imported.")
