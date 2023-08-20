from abc import ABC, abstractmethod
from typing import List


# Abstract interface for image optimization class
class Abs_compressor(ABC):

    @abstractmethod
    def compress(filename: str, ratios: List[int]) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass


# Abstract inteface for image transport stuff
class Abs_transport(ABC):
    @abstractmethod
    def download(filename: str) -> None:
        pass

    @abstractmethod
    def upload(filename: str, url: str) -> None:
        pass


# We need only one method to be declared
# in abstract base class, other would be defined by childs
class Abs_mqtt_manager(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def open_channels(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def check_connection(self) -> None:
        pass


# Base interface for image optimization server class
class Abs_image_server(ABC):

    @abstractmethod
    def __init__(
            self,
            compressor: Abs_compressor,
            image_transport: Abs_transport,
            mqtt_client: Abs_mqtt_manager) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
