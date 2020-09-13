FROM ubuntu:18.04

MAINTAINER liushengli "2001.liu@gmail.com"

RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
RUN update-alternatives --config python3

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD export FLASK_APP=eventapp; export FLASK_ENV=production; flask init-db;python3 run.py

