# Traffic Data Collection

## Project Overview

### Context

In Singapore, in the face of bicycle related traffic accidents, traffic rules require cars to overtake bicycles at a minimum distance of 1.5m.

### Objective

The goal of this project is to collect data on the passing distance of cars to bicycles, as reliable data on this subject of study does not exist. I used two different sensors - a Time of Flight (TOF), and a laser distance sensor to measure the distance of passing vehicles. The sensors were mounted a bike which was used to ride around Singapore roads and collect data.

### Testing

I analyze the results of each test in a separate Jupyter Notebook.

- [TOF Sensor Basic Tests](./data_analysis/TOF_Basic_Tests.ipynb)
- [TOF Sensor Outdoor Tests](./data_analysis/TOF_Outdoor_Tests.ipynb)
- [Laser Sensor Basic Tests](./data_analysis/Laser_Basic_Tests.ipynb)

## Sensor Setup

1. Sensors Used
2. Default Software Setup
3. Using the Sensors with Raspberry Pi
4. Casing Design

### Sensors Used

- [TOF Laser Range Sensor by WaveShare](https://www.waveshare.com/tof-laser-range-sensor.htm)
- [Laser Distance Sensor by Chengdu JRT Meter Technology Co. Ltd](https://www.alibaba.com/product-detail/Laser-Distance-Measuring-Device-100m-Chip_1600877291661.html?spm=a2700.shop_plgr.41413.11.4f9474e2pi4SXS)

### Default Software Setup

- Both the TOF and laser sensors came with their default software for Windows. The [TOF sensor's software](https://www.waveshare.com/wiki/File:Waveshare_TOFAssistant.zip) was found on its [documentation page](https://www.waveshare.com/wiki/TOF_Laser_Range_Sensor). However, the software and documentation of the laser sensor was only provided directly by the manufacturer.
- Before using the software, I needed to the necessary [CP210x USB to UART drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads).
- To connect the TOF sensor to my laptop, I had to purchase a USB to TTL adaptor. The laser sensor came with one pre-installed.
- In addition, for the software to recognize the sensor, I needed to identify which COM port they were connected to. To do this, I needed to activate COM Ports in the Windows device manager by going to: Actions &rarr; Add Legacy Hardware &rarr; And installing Ports (COM & LPT).
- I did not have to adjust the baudrate on the software for the TOF sensor. However, I had to set the baudrate for the laser sensor to 115200bps for it to work with the software.
- Once the software was set up, I could test the sensors to determine that they were working.

### Using the Sensors with Raspberry Pi

To have the sensors collect data while attached to a bike, I needed to attach them to a Raspberry Pi and run a script. Setting this up consisted of 3 parts:

1. Communicating with the sensors via Python.
2. Publishing the data collected to MQTT.
3. Auto-starting the script on boot.

#### Communicating with the Sensors via Python

- Both sensors work by writing and reading bytes to their respective serial ports, which can be extracted and used to find the distance the sensor's measure.
- The [`pyserial`](https://pypi.org/project/pyserial/) module allows communication with serial ports, which in turn allowed me to communicate with the sensors.

    ```bash
    pip install pyserial
    ```

- First, I needed to create a new `serial.Serial()` object and define the correct ports and baudrate. I was stuck for days, but eventually, I realised the TOF and laser sensors needed a baudrate of **921600** and **115200** respectively.

    ```python
    tof_ser = serial.Serial("/dev/ttyS0", 921600)
    laser_ser = serial.Serial("/dev/ttyUSB0", 115200)
    ```

- Next, the sensor would write data to the ports in the form of protcols, which are a string of hexadecimal bytes. The WaveShare documentation gives an example protcol as below.

    ```text
    57 00 ff 00 9e 8f 00 00 ad 08 00 00 03 00 ff 3a
    ```

- The laser sensor contains more functionality and can have different outputs. Therefore, it requires a command to be sent in the form of a hex string representing different bytes. For example, to read distance one time, we send this command using the `Serial.write()` command.

    ```python
    laser_ser.write(b"\xaa\x00\x00\x20\x00\x01\x00\x00\x21")
    ```

- Once the sensors are running and writing data to the serial port, to extract this information and find the distances measured, we need to read the protocol using the `Serial.read(number_of_bytes_to_read)` command. Protocols can differ in length and I had to specify the number of bytes to read from the serial port.

    ```python
    # Reading from the serial port will give a binary hex string like b"\x57\x00\xff" etc.
    protocol = tof_ser.read(16)

    # Using a list comprehension, we can vert it to a list of decimal values
    # representing the respective bytes like [87, 0, 255] etc.
    protocol = [byte for byte in protocol]
    ```

- After reading the protocol, we need to check if it is valid. For both sensors, the last byte of every protocol is a *sum check*. For instance, for the TOF sensor, the sum of all other must equal to the sum check for the protocol to be considered valid and have no errors. We also need to take the modulo of the sum of the bytes because the sum may exceed 256 which is the maximum value for a single byte.

    ```python
    if sum(protocol[:-1]) % 256 == protocol[-1]:
        print("Protocol is valid!")
    ```

- Next, to find useful values like distance, we extract the relevant bytes, convert them back into hex and combine them into a hex string, and convert the hex string into its decimal representation. For instance in the protcol above for the TOF sensor, distance is represented by the bytes in indices 8 to 10 in reverse order.
- This conversion can be found in the `Sensor._to_hex()` and `Sensor._to_hex_string()` in my sensor module.

    ```python
    distance_bytes = protocol[10:7:-1]
    hex_bytes = []

    for byte in distance_bytes:
        # hex(00) -> "\x00"
        # "\x0"[2:] -> "0"
        # "0".zfill(2) -> "00"
        hex_bytes.append(hex(byte)[2:].zfill(2))

    hex_string = "".join(hex_bytes)
    distance = int(hex_string, base=16)
    ```

- I created a base `Sensor` class in [`sensor.py`](./sensor/sensor.py) which has helper methods to read from the sensor and extract relevant bytes from the different protcols. The modules [`tof_sensor.py`](./sensor/tof_sensor.py) and [`laser_sensor.py`](./sensor/laser_sensor.py) inherit from the `Sensor` class and contain methods to use the sensor to measure distances of the TOF and laser sensor respectively based on their different requirements.

#### Publishing to MQTT

- I could now run a Python script to continuously collect data from the sensor. However, it would be good if I could see the data being collected in real time instead of having to to wait for collection to finish before extracting the data from the Raspberry Pi.
- I registered my Raspberry Pi for AWS IoT core and downloaded the AWS IoT Device Python SDK, which contained the necessary certificates that allowed Python scripts to access the AWS IoT platform through MQTT. Essentially, I could send data from the Raspberry Pi over AWS and collect in on my laptop in real time.
- First, I created a [`Publisher()`](./sensor/publish.py) class which contained all the functionality needed to publish data from the Raspberry Pi over to AWS.
- Next, I created a [`subscribe`](./sensor/subscribe.py) script meant to be run on my laptop to view the data in real time. It uses [`paho-mqtt`](https://pypi.org/project/paho-mqtt/) "which enable applications to connect to an MQTT broker to publish messages, and to subscribe to topics and receive published messages".

#### Autostart

- Finally I wrote a main script which collected data and published it to AWS. I needed this script to autostart once the Raspberry Pi booted. For this, I created and enabled a systemd service. The format of the script can be found [here](./sensor/raspberry_pi_autostart/tof_sensor.service).
- I activated the service by running the following commands in the terminal.

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable SERVICE_NAME.service
    ```

- From here, I could troubleshoot if the autostart wasn't working by running by viewing the status of the service.

    ```bash
    sudo systemctl status SERVICE_NAME.service
    ```

- At first, the autostart didn't seem to work no matter what I tried. I finally found that the solution was to have my script sleep for at least 20 seconds before attempting to establish a connection with MQTT. This was because the Raspberry Pi needed time to connect to the internet and would throw an error if it tried to connect to MQTT when there was no internet.

### Casing Design

- After dealing with the software part of things, I needed to design a physical setup to mount on the bicycle. The designs can be found [here](./casing_designs/).
- I decided to use [Decathlon's Universal Smartphone Bike Mount](https://www.decathlon.sg/p/universal-adhesive-garmin-adapter-for-smartphones-triban-8500817.html) to attach the sensor.
- In SolidWorks, I designed a simple frame which I could screw the sensor on. The flat surface of the frame was where I stuck on the bike mount.

    ![Simple Frame](./images/Frame.jpg)

- After some outdoors testing, I realized that the sensor was extremely unreliable when exposed to sunlight. I proceeded to design a shade for the frame to mitigate the collection of missearnt data.

    ![Shade](./images/Shade.jpg)
    ![Frame and Shade](./images/Frame%20and%20Shade.jpg)

- I finally settled on a design which provided enough shade to mitigate the collection of misserant data, but was also compact enough to prevent interference with pedaling the bike.

    ![Final Case 1](./images/Final%20Case%201.jpg)
    ![Final Case 2](./images/Final%20Case%202.jpg)
