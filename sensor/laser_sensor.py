import datetime

import serial


class LaserCommands:
    GET_STATUS = b"\xaa\x80\x00\x00\x80"
    MEASURE_DISTANCE = b"\xaa\x00\x00\x20\x00\x01\x00\x00\x21"


class LaserSensor:
    def __init__(self) -> None:
        self.ser = serial.Serial(port=None, baudrate=115200)
        self._connect_to_device()
        
    @property
    def current_time(self) -> str:
        """
        Returns the current time.
        
        Returns:
            str: Format is HH:MM:SS
        """
        t = str(datetime.datetime.now())
        return t.split(" ")[1].split(".")[0]

    def status(self) -> None:
        """
        Get the status of the module.
        """
        self._send_command(LaserCommands.GET_STATUS)
        protocol = self._read_protocol(9)
        print(protocol)

    def measure_distance(self) -> tuple[int, int]:
        self._send_command(LaserCommands.MEASURE_DISTANCE)
        protocol = self._read_protocol(13)
        distance = self._get_distance_from_protocol(protocol)
        signal_strength = self._get_signal_strength_from_protocol(protocol)
        return distance, signal_strength
    
    def get_data(self) -> str:
        distance, signal_strength = self.measure_distance()
        return f"{self.current_time} {distance} {signal_strength}"
    
    def _connect_to_device(self) -> None:
        ports = ("/dev/ttyUSB0", "/dev/ttyUSB1")
        for port in ports:
            try:
                self.ser.port = port
                self.ser.open()
                return True
            except Exception as e:
                print(f"Wrong port, trying again. {e}")
        return False

    def _send_command(self, command: str) -> None:
        """
        Send a command to the sensor.

        Args:
            command (str): Appropriate command consisting of a string of hexadecimal bytes.
        """
        self.ser.write(command)

    def _read_protocol(self, number_of_bytes: int) -> list[int]:
        """
        Read a the protocol from the sensor.

        Args:
            number_of_bytes (int): Number of bytes to read from the sensor.

        Returns:
            list[int]: List of bytes expressed in decimal.
        """
        return [byte for byte in self.ser.read(number_of_bytes)]

    def _is_valid_protocol(self, protocol: list[int]) -> bool:
        return sum(protocol[1:-1]) == protocol[-1]

    def _get_distance_from_protocol(self, protocol: list[int]) -> int:
        distance_bytes = protocol[6:10]
        hex_string = "".join(self._to_hex(byte) for byte in distance_bytes)
        return int(hex_string, base=16)
    
    def _get_signal_strength_from_protocol(self, protocol: list[int]) -> int:
        signal_strength_bytes = protocol[10:12]
        hex_string = "".join(self._to_hex(byte) for byte in signal_strength_bytes)
        return int(hex_string, base=16)
    
    def _to_hex(self, byte: int) -> str:
        return hex(byte)[2:].zfill(2)
    
    
if __name__ == "__main__":
    sensor = LaserSensor()
    print(sensor.measure_distance())
