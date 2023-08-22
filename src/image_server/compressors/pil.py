from typing import List

from PIL import Image, UnidentifiedImageError

from src.common_stuff.interfaces import Abs_compressor
from src.common_stuff.logger import get_logger, setup_logger


# Default implementation of image compressor
class PIL_compressor(Abs_compressor):

    def __init__(
        self,
        images_dir: str,
        compressed_images_dir: str
    ) -> None:
        self.images_dir = images_dir
        self.compressed_images_dir = compressed_images_dir
        self.logger = get_logger(self.__class__.__name__)
        setup_logger(logger=self.logger)

    def compress(self, filename: str, ratios: List[int]) -> None:
        try:
            for ratio in ratios:
                name = filename.split('.')[0]
                ext = filename.split('.')[-1]
                full_path = f'{self.images_dir}/{filename}'
                img = Image.open(full_path)
                img.save(
                    f'{self.compressed_images_dir}/'
                    f'{name}_{ratio}.{ext}',
                    optimize=True,
                    quality=ratio
                )
        # Image could be corrupted or not valid
        except UnidentifiedImageError:
            self.logger.error("unknown file format.")
            pass

    def stop(self):
        pass
