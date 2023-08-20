FROM python:3.9-slim-buster

EXPOSE 8000
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DL_CHUNK_SIZE 4096
ENV PIL_PROCESS_COUNT 8
ENV MQTT_HOST rabbitmq


COPY ./src  ./src
COPY ./main.py ./
RUN rm /app/src/web_api/ -rf
RUN mkdir /app/src/uploaded_images
RUN mkdir /app/src/optimized_images
COPY ./dockerfiles/image_server/requirements_pil.txt ./

RUN pip install -r requirements_pil.txt

ENV ORIG_IMG_DIR "/app/src/uploaded_images"
ENV OPT_IMG_DIR "/app/src/optimized_images"
CMD [ "python3", "main.py"]
