# Raspberry Pi Code

The code for the Raspberry Pi consisted of 3 parts: interacting with the sensors, publishing the data, and other auxilliary code.

## Sensor Code

Both the TOF and laser sensors could be communicated with via serial ports in very similar ways. Therefore, I split the code for the sensors into 3 modules. First, I created a base class [`sensor.py`](./sensor/sensor.py) which housed the `Sensor` class to be inherited from. The sensor class contained the basic methods used by both TOF and laser sensors to read and process protocols.

[`laser_sensor.py`](./sensor/laser_sensor.py) and [`tof_sensor.py`](./sensor/tof_sensor.py) contain the classes `LaserSensor` and `TOFSensor` respectively, which inherit from `Sensor`. Both of these classes could be used interchangably to interact with whichever sensor was needed.

## Publishing Code

I also needed to publish my data via MQTT to AWS. Instead of building in the publishing feature within each sensor module, I created a [`publish.py`](./sensor/publish.py) which did this indpenedently. [`constants.py`](./sensor/constants.py) contained the constants needed to initialize the `Publisher` module. I could then combine the sensor and publishing object in a very clean way like so.

```python
from laser_sensor import LaserSensor
from publish import Publisher

sensor = LaserSensor()
publisher = Publisher()

data = sensor.get_data()
publisher.publish(data)
```

I also have a [`subscribe.py`](./sensor/subscribe.py) module meant to be run on another computer. This script would help to receive the data in real time that is being published.

## Auxilliary Code

Finally, I created some auxilliary functions in [`utils.py`](./sensor/utils.py). The most significant one would be `wait_for_internet`, which would ensure a successful connection via MQTT.
