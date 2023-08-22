from src.common_stuff.interfaces import Abs_is_mqtt_client
from src.common_stuff.mqtt_base import BaseMQTTManager


class IS_MQTT_client(Abs_is_mqtt_client, BaseMQTTManager):

    async def consume(self, clb) -> None:
        await self.inqueue.consume(clb)
