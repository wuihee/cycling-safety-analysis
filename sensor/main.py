import logging

from laser_sensor import LaserSensor
from publish import Publisher
from tof_sensor import TOFSensor
from utils import cd_to_parent_dir, wait_for_internet, write_to_file

cd_to_parent_dir()
logging.basicConfig(filename="./files/tof.log", level=logging.DEBUG)
logging.debug("Starting...")

wait_for_internet()
logging.debug("Connected to internet!")

# Change sensor to either LaserSensor() or TOFSensor() depending on which you're using.
sensor = LaserSensor()
publisher = Publisher()

while True:
    data = sensor.get_data()

    if data == "Invalid Protocol":
        publisher.publish("Invalid protocol encountered. Stopping.")

    if data:
        publisher.publish(data)
        write_to_file("./files/saved_data.txt", data)
        print(data)
