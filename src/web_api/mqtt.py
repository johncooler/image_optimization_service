#!/usr/bin/env python

import aio_pika

from src.common_stuff.interfaces import Abs_wa_mqtt_client
from src.common_stuff.mqtt_base import BaseMQTTManager


class MQTT_Client(Abs_wa_mqtt_client, BaseMQTTManager):

    # Routine that will be invoked to notify
    # image server about new data
    async def push_to_queue(self, message: str) -> None:
        # Set publisher with persistent mode
        await self.outchannel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=self.output_channel_name,
        )

    # def pull(self, ch, method, properties, body) -> None:
    #     self.queue.put(body)

    # def get_info(self):
    #     self.inchannel.basic_consume(
    #         queue=self.input_channel_name,
    #         on_message_callback=self.pull,
    #         auto_ack=True
    #     )
    #     self.inchannel.start_consuming()
