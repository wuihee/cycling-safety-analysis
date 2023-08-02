import logging

from publish import Publisher
from tof_sensor import TOFSensor
from laser_sensor import LaserSensor
from utils import cd_to_parent_dir, write_to_file

cd_to_parent_dir()
logging.basicConfig(filename="./files/tof.log", level=logging.DEBUG)
logging.debug("Starting...")

# We need to sleep for 20s to wait for the Raspberry Pi to connect to the internet.
publisher = Publisher(sleep=20)

# Change sensor to either LaserSensor() or TOFSensor() depending on which you're using.
sensor = LaserSensor()

while True:
    data = sensor.get_data()

    if data == "Invalid Protocol":
        publisher.publish("Invalid protocol encountered. Stopping.")

    if data:
        publisher.publish(data)
        write_to_file("./files/saved_data.txt", data)
        print(data)
