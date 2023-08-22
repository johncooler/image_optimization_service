#!/usr/bin/env python
import asyncio
import json
import os
from typing import List

from fastapi import (FastAPI, HTTPException, Query, Request, Response,
                     UploadFile, WebSocket)
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src import (ingoing_queue_name, mqtt_host, optimized_images_dir,
                 outgoing_queue_name, uploaded_images_dir)
from src.common_stuff.interfaces import Abs_wa_mqtt_client
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


@app.on_event("startup")
async def open_channels():
    await notifier.open_channels()


@app.on_event("shutdown")
async def close_sessions(notifier: Abs_wa_mqtt_client = notifier) -> None:
    # Would be executed before exit
    logger.info("Close MQTT session...")
    await notifier.connection.close()


# Directory with user photos
app.mount(
    "/original_photos",
    StaticFiles(directory=uploaded_images_dir),
    name="static"
)
templates = Jinja2Templates(directory="src/web_api/templates")
app.mount(
    "/pictures",
    StaticFiles(directory=optimized_images_dir),
    name="static"
)


# @app.websocket("/status")
# async def ws_get_status(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = notifier.queue.get()
#         websocket.send_text(data)


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
            # I leaved that method for S3 bucket use possibility
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


# That function is just like shorthand to download optimized pictures,
# there shouldn't be such methods, it's frontend app responsibility
@app.get("/optimized_photos/", response_class=HTMLResponse)
async def listing(request: Request):
    files = os.listdir(optimized_images_dir)
    files_paths = sorted([
        f"/pictures/{f}"
        for f in files])
    return templates.TemplateResponse(
        "list_files.html", {"request": request, "files": files_paths}
    )


@app.get("/download/{picture}")
async def image_download(picture: str, quality: int = 100):
    picture_name = picture.split('.')[0]
    picture_ext = picture.split('.')[-1]
    path_to_file = f"{optimized_images_dir}/{picture_name}_{quality}.{picture_ext}"
    if not os.path.exists(path_to_file):
        raise HTTPException(status_code=404, detail="Item not found")
    return FileResponse(path_to_file)
