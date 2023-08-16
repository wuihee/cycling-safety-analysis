from laser_sensor import LaserSensor
from publish import Publisher

publisher = Publisher()
sensor = LaserSensor(publisher)
sensor.measure_distance_continuous()
