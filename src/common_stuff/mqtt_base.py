import aio_pika

from src.common_stuff.interfaces import Abs_mqtt_manager
from src.common_stuff.logger import get_logger, setup_logger


# Common parent class for both WebAPI and ImageServer
# class implementations
class BaseMQTTManager(Abs_mqtt_manager):

    def __init__(
        self,
        mqtt_host: str = 'localhost',
        port: int = 5672,
        blocked_connection_timeout: int = 60,
        input_channel_name: str = None,
        output_channel_name: str = None
    ) -> None:
        self.logger = get_logger(self.__class__.__name__)
        setup_logger(logger=self.logger)
        # Establish connection with MQTT server
        self.host = mqtt_host
        self.port = port
        self.timeout = blocked_connection_timeout
        self.logger.info("Connection with MQTT server established.")
        self.input_channel_name = input_channel_name
        self.output_channel_name = output_channel_name
        self.inchannel: aio_pika.Channel = None
        self.outchannel: aio_pika.Channel = None
        self.channels: list[aio_pika.Channel] = []

    async def open_channels(self) -> None:
        self.connection = await aio_pika.connect_robust(
            host=self.host,
            port=self.port,
            timeout=self.timeout,
        )
        # Declare channels to interact with MQTT server
        # async with self.connection:
        # Creating channels
        self.inchannel = await self.connection.channel()
        # Will take no more than 3 messages in advance
        await self.inchannel.set_qos(prefetch_count=3)
        self.inqueue = await self.inchannel.declare_queue(
            self.input_channel_name,
            durable=True,
            auto_delete=True)
        self.channels.append(self.inchannel)
        self.outchannel = await self.connection.channel()
        # Will take no more than 3 messages in advance
        await self.outchannel.set_qos(prefetch_count=3)
        self.outqueue = await self.outchannel.declare_queue(
            self.output_channel_name,
            durable=True,
            auto_delete=True)
        self.channels.append(self.outchannel)
