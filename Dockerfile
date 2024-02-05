FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt
