import concurrent
import json
import logging

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from constants import AWSConstants


class Publisher:
    def __init__(self) -> None:
        """
        Intialize an MQTTT connection to send publish messages to.
        """
        self.mqtt_connection = self.connect()

    def connect(self) -> mqtt.Connection:
        """
        Create an MQTT connection object.

        Returns:
            mqtt.Connection: Returns the connection object.
        """
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=AWSConstants.ENDPOINT,
            cert_filepath=AWSConstants.AWS_CERTIFICATE,
            pri_key_filepath=AWSConstants.AWS_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=AWSConstants.AWS_ROOT_CA,
            client_id=AWSConstants.CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6,
        )

        future_connection = mqtt_connection.connect()
        if self.resolve_future_connection(future_connection):
            return mqtt_connection

    def resolve_future_connection(
        self, future_connection: concurrent.futures.Future
    ) -> bool:
        """
        Resolve a future connection object.

        Args:
            (concurrent.futures.Future) future_connection: Future created by MQTT connection.

        Returns:
            bool: Returns true if connection was successfully resolved else false.
        """
        try:
            future_connection.result()
            logging.debug("Connection Succuessful!")
            return True

        except Exception as e:
            logging.error(f"Unable to connect: {e}")
            return False

    def publish(self, message: str) -> None:
        """
        Publish a message to MQTT topic.

        Args:
            (str) message: Message to be published.
        """
        self.mqtt_connection.publish(
            topic=AWSConstants.TOPIC,
            payload=json.dumps(message),
            qos=mqtt.QoS.AT_LEAST_ONCE,
        )

    def disconnect(self) -> None:
        """
        Disconnect from MQTT connection.
        """
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()


if __name__ == "__main__":
    print("publish module to be imported.")
