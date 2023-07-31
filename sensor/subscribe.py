import paho.mqtt.client as mqtt
from constants import Constants
from utils import cd_to_parent_dir

cd_to_parent_dir()


def write_to_file(filename, message) -> None:
    with open(filename, "a") as file:
        file.write(message + "\n")


def decode_message(message) -> int:
    message = message.decode()
    message = message.strip('"')
    return message


def on_connect(client, userdata, flags, rc) -> None:
    """Callback function for when client receives a CONNACK response from the server."""
    print(f"Connected with result code {rc}")
    client.subscribe(Constants.TOPIC)


def on_message(client, userdata, msg) -> None:
    """Callback for when a PUBLISH message is received from the server."""
    distance = decode_message(msg.payload)
    print(distance)
    write_to_file("./files/tof_data.txt", distance)


def on_subscribe(client, userdata, mid, granted_qos) -> None:
    print(f"Subscribed to topic {Constants.TOPIC} successfully")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.tls_set(Constants.AWS_ROOT_CA, certfile=Constants.AWS_CERTIFICATE, keyfile=Constants.AWS_PRIVATE_KEY)
client.connect(Constants.ENDPOINT, Constants.PORT, keepalive=60)
client.loop_forever()
