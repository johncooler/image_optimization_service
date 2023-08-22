from abc import ABC, abstractmethod
from typing import Callable, List


# Abstract interface for image optimization class
class Abs_compressor(ABC):

    @abstractmethod
    def compress(filename: str, ratios: List[int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError


# Abstract inteface for image transport stuff
class Abs_transport(ABC):

    # Method to download file from resource
    @abstractmethod
    def download(self, file_path: str = None, url: str = None) -> None:
        raise NotImplementedError

    # Method to upload file to resource
    @abstractmethod
    def upload(self, file_path: str = None, url: str = None) -> None:
        raise NotImplementedError


# We need only one method to be declared
# in abstract base class, other would be defined by childs
class Abs_mqtt_manager(ABC):
    @abstractmethod
    def __init__(self, mqtt_host: str, port: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def open_channels(self) -> None:
        raise NotImplementedError


# Different abstraction for Web API
class Abs_wa_mqtt_client(Abs_mqtt_manager):

    @abstractmethod
    async def push_to_queue(self, message: str) -> None:
        raise NotImplementedError


# Different abstraction for Image Server
class Abs_is_mqtt_client(Abs_mqtt_manager):

    @abstractmethod
    async def consume(self, callback: Callable) -> None:
        raise NotImplementedError


# Base interface for image optimization server class
class Abs_image_server(ABC):

    # We gonna use Facade pattern to organize objects
    # and to provide a simple point of access
    @abstractmethod
    def __init__(
            self,
            compressor: Abs_compressor,
            image_transport: Abs_transport,
            mqtt_client: Abs_is_mqtt_client) -> None:
        raise NotImplementedError

    # Entrypoint
    @abstractmethod
    async def run(self) -> None:
        raise NotImplementedError
