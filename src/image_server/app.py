import os
import sys

from src import (ingoing_queue_name, mqtt_host, optimized_images_dir,
                 outgoing_queue_name, process_count, uploaded_images_dir)
from src.common_stuff.mqtt_base import BaseMQTTManager
from src.common_stuff.transport import TransportMock
from src.image_server.compressors.pil import PIL_compressor
from src.image_server.compressors.pil_mp import PIL_MP_compressor
from src.image_server.server import ImageServer


def app():
    try:
        # It's nothing more that just empty function that is
        # reserved to implement downloading files over network
        # but save interface compatibility
        img_transport_mock = TransportMock()
        # We want to decide what kind of compression
        # implementation should be used
        if os.cpu_count() > 1:
            compressor = PIL_MP_compressor(
                images_dir=uploaded_images_dir,
                compressed_images_dir=optimized_images_dir,
                processes=process_count
            )
        else:
            compressor = PIL_compressor(
                images_dir=uploaded_images_dir,
                compressed_images_dir=optimized_images_dir
            )
        # Base MQTT client initialization
        mqtt_client = BaseMQTTManager(
            input_channel_name=ingoing_queue_name,
            output_channel_name=outgoing_queue_name,
            mqtt_host=mqtt_host)
        # Main server instance init
        image_server = ImageServer(
            compressor=compressor,
            mqtt_client=mqtt_client,
            image_transport=img_transport_mock
        )
        # Entrypoint
        image_server.run()
    except KeyboardInterrupt:
        image_server.compressor.stop()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
