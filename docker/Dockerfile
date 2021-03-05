FROM python:3.7.6-slim

ARG WORKING_DIR=/usr/src/app

WORKDIR $WORKING_DIR


RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    nano \
    libsndfile1 \
    build-essential \
    ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt --disable-pip-version-check --no-cache-dir

COPY . .

CMD ["python3"]