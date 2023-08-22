#!/usr/bin/env python
import pika

from src.common_stuff.mqtt_base import BaseMQTTManager
from src.common_stuff.interfaces import Abs_wa_mqtt_client
from asyncio import Lock


class MQTT_Client(Abs_wa_mqtt_client, BaseMQTTManager):

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
        super().__init__(
            mqtt_host,
            port,
            retry_delay,
            heartbeat,
            blocked_connection_timeout,
            input_channel_name,
            output_channel_name)
        self.open_channels()
        self.check_connection()
        self.lock = Lock()

    # Routine that will be invoked to notify
    # image server about new data
    async def push_to_queue(self, message: str) -> None:
        # Set publisher with persistent mode
        async with self.lock:
            self.outchannel.basic_publish(
                exchange='',
                routing_key=self.output_channel_name,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
                body=message
            )