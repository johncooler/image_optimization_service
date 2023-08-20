import pika
from pika import exceptions

from src.common_stuff.logger import get_logger, setup_logger
from src.common_stuff.interfaces import Abs_mqtt_manager


# Common parent class for both WebAPI and ImageServer
# class implementations
class BaseMQTTManager(Abs_mqtt_manager):

    def __init__(
        self,
        mqtt_host: str,
        port: int = 5672,
        retry_delay: int = 5,
        heartbeat: int = 0,
        blocked_connection_timeout: int = 60,
        input_channel_name: str = None,
        output_channel_name: str = None
    ) -> None:
        self.logger = get_logger(self.__class__.__name__)
        setup_logger(logger=self.logger)
        # Establish connection with MQTT server
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=mqtt_host,
                port=port,
                retry_delay=retry_delay,
                heartbeat=heartbeat,
                blocked_connection_timeout=blocked_connection_timeout
            )
        )
        self.logger.info("Connection with MQTT server established.")
        self.input_channel_name = input_channel_name
        self.output_channel_name = output_channel_name
        self.channels = []

    def open_channels(self) -> None:
        # Declare channels to interact with MQTT server
        self.inchannel = self.connection.channel()
        self.channels.append(self.inchannel)
        self.outchannel = self.connection.channel()
        self.channels.append(self.outchannel)
        # Declare ingoing and outgoing queues
        self.ingoing = self.inchannel.queue_declare(
            queue=self.input_channel_name, durable=True)
        self.outgoing = self.outchannel.queue_declare(
            queue=self.output_channel_name, durable=True)
        self.logger.info("Channels was opened successfully.")

    def check_connection(self) -> None:
        if self.connection.is_closed:
            raise exceptions.ConnectionClosed
        for ch in self.channels:
            if ch.is_closed:
                raise exceptions.ChannelClosed
