FROM docker.io/python:3.11-bullseye

WORKDIR /usr/src/app

COPY misc/sources.list /etc/apt/sources.list
COPY misc/geckodriver-v0.33.0-linux64.tar.gz /tmp

COPY . .

ENV PIP_INDEX_URL https://pypi.tuna.tsinghua.edu.cn/simple

RUN tar -zxvf /tmp/geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin & \
    rm /tmp/geckodriver-v0.33.0-linux64.tar.gz

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends firefox-esr && \
    apt-get clean && \
    pip install -U pip && \
    pip install -r ./requirements.txt
