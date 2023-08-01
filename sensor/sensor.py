import datetime

import serial


class Sensor:
    def __init__(self) -> None:
        self.ser = serial.Serial(port=None, baudrate=self.BAUDRATE)
