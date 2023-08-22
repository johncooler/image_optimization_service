#!/usr/bin/env python3
import asyncio
import json

import aio_pika

from src.common_stuff.interfaces import (Abs_compressor, Abs_image_server,
                                         Abs_is_mqtt_client, Abs_transport)
from src.common_stuff.logger import get_logger, setup_logger


class ImageServer(Abs_image_server):

    def __init__(
        self,
        compressor: Abs_compressor,
        image_transport: Abs_transport,
        mqtt_client: Abs_is_mqtt_client,
    ) -> None:
        self.logger = get_logger(self.__class__.__name__)
        setup_logger(logger=self.logger)
        # Attach instances
        self.mqtt_client = mqtt_client
        self.compressor = compressor
        # That instance could be both mock
        # or working implementation
        self.transport = image_transport
        # # Set channels
        # self.mqtt_client.open_channels()
        # self.mqtt_client.check_connection()

    async def pull_from_queue(
        self,
        message: aio_pika.abc.AbstractIncomingMessage,
    ) -> None:
        async with message.process():
            decoded_body = message.body
            decoded_body = json.loads(decoded_body)
            filename = decoded_body['filename']
            ratios = decoded_body["ratios"]
            self.transport.download(file_path=filename, url=filename)
            self.logger.info(f"Received {filename} image")
            self.compressor.compress(
                filename=filename,
                ratios=ratios
            )

    # Main entrypoint of class
    async def run(self) -> None:
        await self.mqtt_client.open_channels()
        await self.mqtt_client.consume(self.pull_from_queue)

        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await self.mqtt_client.connection.close()
