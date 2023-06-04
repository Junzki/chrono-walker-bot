FROM docker.io/python:3.11-bullseye

WORKDIR /usr/src/app

COPY misc/sources.list /etc/apt/sources.list

COPY . .

ENV PIP_INDEX_URL https://pypi.tuna.tsinghua.edu.cn/simple

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends firefox-esr && \
    apt-get clean && \
    pip install -U pip && \
    pip install -r ./requirements.txt && \
    bash ./setup.sh
