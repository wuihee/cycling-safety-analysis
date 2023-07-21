# TOF Sensor Data Collection

## Project Overview

### Context

In Singapore, in the face of bicycle related traffic accidents, traffic rules require cars to overtake bicycles at a minimum distance of 1.5m.

### Objective

The goal of this project is to collect data on the passing distance of cars to bicycles, as reliable data on this subject of study does not exist. I use a Time of Flight (TOF) to collect the data, which uses infrared technology to measure distance accurately. The sensor is mounted a bike which is used to ride around Singapore roads, collecting data which can be further analyzed.

## Setting Up the TOF Sensor

1. Setup
2. Basic Tests
3. Raspberry Pi Setup
4. Casing Design
5. Outdoors Testing

### Setup

- The first objective was to test the standalone distance measuring capabilities of the sensor.
- To set it up on Windows, I first installed the [software](https://www.waveshare.com/wiki/File:Waveshare_TOFAssistant.zip) from the [documentation](https://www.waveshare.com/wiki/TOF_Laser_Range_Sensor).
- I then purchased a USB to TTL adaptor to connect the sensor to my Windows laptop.
- For the sensor to work, I needed to install the [CP210x USB to UART drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads).

### Basic Tests

- Using the software provided, I tested the distance measuring capabilities of the sensor at intervals of 0.5 meters, from 0.5 meters to 5.0 meters.
- I quickly realized that the sensor would lose a lot of it's accuracy in bright daylight.
- The default software allowed me to export the data in an excel file format, which I proceeded to extract the data from and graph using Matplotlib.
- The data analysis can be found in my Jupyter Notebook.

### Raspberry Pi Setup

- To run the sensor on a Raspberry Pi, I downloaded the [demo code](https://www.waveshare.com/wiki/TOF_Laser_Range_Sensor#Resources) provided by the documentation, and enabled to necessary [serial port settings](https://www.waveshare.com/wiki/TOF_Laser_Range_Sensor#Working_with_Raspberry_Pi).
- Unfortunately, the code didn't work, and with a lack of Python API documentation, I was left to trial and error until I found a solution:

    ```python
    ser = serial.Serial("/dev/ttyS0", 921600)
    ```

- This line of code was needed to enable UART communication between the sensor and Raspberry Pi.
- I cleaned up the code and modularized it into a [`Sensor()`](./tof_sensor/sensor.py) class.
- Next, I wanted a way to see the data on the fly as it was being collected, and not have to wait for collection to finish before extracting the data from the Raspberry Pi.
- I registered my Raspberry Pi for AWS IoT core, and allowed it to publish data via MQTT. I could then subscribe to the MQTT topic on my laptop, and see the data as it was being collected in real time. For this, I created a [`Publisher()`](./tof_sensor/publish.py) class and a [`subscribe`](./tof_sensor/subscribe.py) script.

### Casing Design

- After dealing with the software part of things, I needed to design a physical setup to mount on the bicycle.
- I decided to use [Decathlon's Universal Smartphone Bike Mount](https://www.decathlon.sg/p/universal-adhesive-garmin-adapter-for-smartphones-triban-8500817.html) to attach the sensor.
- In SolidWorks, I designed a simple frame which I could screw the sensor on. The flat surface of the frame was where I stuck on the bike mount.
- After some outdoors testing, I realized that the sensor was extremely unreliable when exposed to sunlight. I proceeded to go through another design, before settling on one which not only provided enough shade to mitigate the collection of misserant data, but was also compact enough to prevent interference with pedaling the bike.


### Outdoors Testing
