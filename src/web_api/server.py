#!/usr/bin/env python
import json
import os
from typing import List

from fastapi import FastAPI, HTTPException, Query, Response, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src import (ingoing_queue_name, mqtt_host, optimized_images_dir,
                 outgoing_queue_name, uploaded_images_dir)
from src.common_stuff.interfaces import Abs_mqtt_manager
from src.common_stuff.transport import TransportMock as transport
from src.web_api import logger
from src.web_api.misc import save_file_to_disk
from src.web_api.mqtt import MQTT_Client

notifier = MQTT_Client(
    input_channel_name=outgoing_queue_name,
    output_channel_name=ingoing_queue_name,
    mqtt_host=mqtt_host
)


app = FastAPI()


@app.on_event("shutdown")
async def close_sessions(notifier: Abs_mqtt_manager) -> None:
    # Would be executed before exit
    logger.info("Close MQTT session...")
    notifier.connection.close()


# Directory with user photos
app.mount(
    "/original_photos",
    StaticFiles(directory=uploaded_images_dir),
    name="static"
)


@app.post("/upload/")
async def image_upload(
    files: List[UploadFile],
    quality: List[int] = Query(default=[100, 75, 50, 25])
):
    try:
        # We wanna use checksums of the file to
        # get unique identifier
        hashes = []
        for file in files:
            new_name = await save_file_to_disk(file)
            hashes.append(new_name)
            message = {
                "filename": new_name,
                "ratios": quality
            }
            transport.upload(new_name)
            await notifier.push_to_queue(
                message=json.dumps(message)
            )
        resp_body = json.dumps({"file_ids": hashes})
        return Response(content=resp_body, status_code=200)
    except Exception as err:
        logger.error(err)
        return Response(status_code=500)
    finally:
        await file.close()


@app.get("/download/{picture}")
async def image_download(picture: str, quality: int = 100):
    picture_name = picture.split('.')[0]
    picture_ext = picture.split('.')[-1]
    path_to_file = f"{optimized_images_dir}/{picture_name}_{quality}.{picture_ext}"
    if not os.path.exists(path_to_file):
        raise HTTPException(status_code=404, detail="Item not found")
    return FileResponse(path_to_file)
