import serial


class LaserCommands:
    GET_STATUS = b"\xaa\x80\x00\x00\x80"
    DISTANCE = b"\xaa\x00\x00\x20\x00\x01\x00\x00\x21"


class LaserSensor:
    def __init__(self) -> None:
        self.PORT = "/dev/ttyUSB0"
        self.BAUDRATE = 115200
        self.ser = serial.Serial(self.PORT, self.BAUDRATE)
        self.ser.reset_input_buffer()

    def status(self) -> None:
        """
        Get the status of the module.
        """
        self._send_command(LaserCommands.GET_STATUS)
        protocol = self._read_protocol(9)
        print(self._convert_protocol_to_list(protocol))

    def measure_distance(self) -> int:
        self._send_command(LaserCommands.DISTANCE)
        protocol = self._read_protocol(13)
        protocol = self._convert_protocol_to_list(protocol)
        return self._get_distance_from_protocol(protocol)

    def _send_command(self, command: str) -> None:
        """
        Send a command to the sensor.

        Args:
            command (str): Appropriate command consisting of a string of hexadecimal bytes.
        """
        self.ser.write(command)

    def _read_protocol(self, number_of_bytes: int) -> str:
        """
        Read a the protocol from the sensor.

        Args:
            number_of_bytes (int): Number of bytes to read from the sensor.

        Returns:
            str: String of bytes in hexademical.
        """
        protocol = self.ser.read(number_of_bytes)
        return protocol

    def _convert_protocol_to_list(self, protocol: str) -> list[str]:
        return [f"{byte:02X}" for byte in protocol]

    def _get_distance_from_protocol(self, data: list[str]) -> int:
        return int("".join(data[7:10]), base=16)


laser = LaserSensor()
distance = laser.measure_distance()
print(distance / 1000)
