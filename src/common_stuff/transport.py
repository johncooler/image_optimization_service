from src.common_stuff.interfaces import Abs_transport
import requests
from src import optimized_images_dir


# Just mocking for future implementations
class TransportMock(Abs_transport):

    def __init__(self, *args, **kwargs) -> None:
        pass

    def download(self, *args, **kwargs) -> None:
        pass

    def upload(self, *args, **kwargs) -> None:
        pass


class HTTP_Transport(Abs_transport):

    def __init__(
        self,
        host: str = None,
        port: int = None,
        scheme: str = 'http://'
        # download_path =
    ) -> None:
        self.base_url = f"{scheme}{host}:{port}"
        self.download_session = requests.Session()
        self.upload_session = requests.Session()

    def download(self, file_path: str = None, url: str = None) -> None:
        if url[0] != '/':
            url = '/' + url
        resp = self.session.get(url=f"{self.base_url}{url}")
        with open(f"{optimized_images_dir}{file_path}", "w") as output_file:
            output_file.write(resp.content)

    def upload(self, file_path: str = None, url: str = None) -> None:
        # self.upload_session.post()
        pass
