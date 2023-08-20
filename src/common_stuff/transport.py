from src.common_stuff.interfaces import Abs_transport


# Just mocking for future implementations
class TransportMock(Abs_transport):

    def __init__(self, *args, **kwargs) -> None:
        pass

    def download(self, *args, **kwargs) -> None:
        pass

    def upload(self, *args, **kwargs) -> None:
        pass
