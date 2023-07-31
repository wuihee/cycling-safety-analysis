import logging

from publish import Publisher
from tof_sensor import TOFSensor
from utils import cd_to_parent_dir, restart_script, write_to_file

cd_to_parent_dir()
logging.basicConfig(filename="./files/tof.log", level=logging.DEBUG)
logging.debug("Starting...")

publisher = Publisher(sleep=0)
sensor = TOFSensor()

while True:
    data = sensor.get_data()

    if data == "Invalid Protocol":
        publisher.publish("Invalid protocol encountered. Stopping.")
        restart_script()

    if data:
        publisher.publish(data)
        write_to_file("./files/saved_data.txt", data)
        print(data)
