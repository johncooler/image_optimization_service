from typing import Callable

from src.common_stuff.mqtt_base import BaseMQTTManager

from src.common_stuff.interfaces import Abs_is_mqtt_client


class IS_MQTT_client(Abs_is_mqtt_client, BaseMQTTManager):

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

    def consume(self, callback: Callable):
        self.inchannel.basic_consume(
            queue=self.input_channel_name,
            on_message_callback=callback,
            auto_ack=True
        )
        self.logger.info('Waiting for messages. To exit press CTRL+C')
        self.inchannel.start_consuming()
