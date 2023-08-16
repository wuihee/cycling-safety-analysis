import logging

from laser_sensor import LaserSensor
from publish import Publisher
from utils import cd_to_parent_dir, wait_for_internet, write_to_file

cd_to_parent_dir()
logging.basicConfig(filename="./files/tof.log", level=logging.DEBUG)
logging.debug("Starting...")

wait_for_internet()
logging.debug("Connected to internet!")

publisher = Publisher()
sensor = LaserSensor(publisher)

while True:
    data = sensor.get_data()
    publisher.publish(data)
    write_to_file("./files/saved_data.txt", data)
    print(data)
