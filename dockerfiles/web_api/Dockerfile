FROM python:3.9-slim-buster

EXPOSE 8000
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DL_CHUNK_SIZE 4096
ENV PIL_PROCESS_COUNT 8
ENV MQTT_HOST rabbitmq


COPY dockerfiles/web_api/requirements_web.txt ./
RUN pip install -r requirements_web.txt

COPY ./src ./src
RUN rm /app/src/image_server/ -rf
RUN mkdir -p /app/src/uploaded_images
RUN mkdir -p /app/src/optimized_images



ENV ORIG_IMG_DIR "/app/src/uploaded_images"
ENV OPT_IMG_DIR "/app/src/optimized_images"
ENTRYPOINT bash -c "gunicorn src.web_api.server:app -w 2 -k uvicorn.workers.UvicornWorker -b $API_HOST:$API_PORT"


