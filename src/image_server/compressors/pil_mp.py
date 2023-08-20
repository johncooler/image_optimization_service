from multiprocessing import Pool, Queue
from typing import List

from src.image_server.compressors.pil import PIL_compressor


# Some multiprocessing alternative that is
# successor of PIL_compressor
# Extended implementation allows to serve more within
# the same time
class PIL_MP_compressor(PIL_compressor):

    def __init__(
        self,
        images_dir: str,
        compressed_images_dir: str,
        processes: int = 4
    ) -> None:
        super().__init__(images_dir, compressed_images_dir)
        # Queue allows to control workers and delegate tasks
        self.queue = Queue(maxsize=128)
        self.pool = Pool(processes=processes, initializer=self._task)
        self.logger.info("Process pool initialized.")

    def _task(self) -> None:
        while True:
            args = self.queue.get()
            super().compress(filename=args[0], ratios=args[1])

    def compress(self, filename: str, ratios: List[int]) -> None:
        for ratio in ratios:
            self.queue.put([filename, [ratio]])

    def stop(self):
        self.logger.info("Process pool closing...")
        self.pool.close()
        self.pool.join()
