#!/usr/bin/env python
import pika

from src.common_stuff.mqtt_base import BaseMQTTManager
from asyncio import Lock


class MQTT_Client(BaseMQTTManager):
    def __init__(
            self,
            input_channel_name,
            output_channel_name,
            mqtt_host) -> None:
        super().__init__(
            input_channel_name=input_channel_name,
            output_channel_name=output_channel_name,
            mqtt_host=mqtt_host)
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