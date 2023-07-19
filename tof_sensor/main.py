import logging

from publish import Publisher
from sensor import Sensor
from utils import cd_to_parent_dir, write_to_file

cd_to_parent_dir()
logging.basicConfig(filename="./files/tof.log", level=logging.DEBUG)
logging.debug("Starting...")

publisher = Publisher(sleep=20)
sensor = Sensor()

while True:
    data = sensor.get_data()

    if data == "Invalid Protocol":
        publisher.publish("Invalid protocol encountered. Stopping.")
        break

    if data:
        publisher.publish(data)
        write_to_file("./files/saved_data.txt", data)
        print(data)
