import hashlib
from os import rename

import aiofiles
from fastapi import UploadFile

from src import async_download_chunk_size
from src import uploaded_images_dir as files_dir


# Asynchronous method that uploads and saves file
async def save_file_to_disk(file: UploadFile) -> None:
    # Original filename from POST request
    orig_filename = file.filename
    # Get file format
    file_format = orig_filename.split('.')[-1]
    # Where to save
    file_path = f"{files_dir}/{orig_filename}"
    async with aiofiles.open(file_path, 'wb') as out_file:
        m = hashlib.new('sha256')
        # async read chunk
        while content := await file.read(async_download_chunk_size):
            await out_file.write(content)  # async write chunk
            m.update(content)
        # Get full SHA256 sums to rename file
        sha256sum = m.hexdigest()[:16]
        new_name = f"{sha256sum}.{file_format}"
        new_file_path = f"{files_dir}/{new_name}"
        rename(file_path, new_file_path)
    return new_name
