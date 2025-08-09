FROM docker.io/python:3.13-bullseye

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends firefox-esr build-essential && \
    apt-get clean && \
    pip install -U pip && \
    pip install -r ./requirements.txt && \
    pip install uWSGI && \
    bash ./setup.sh

# Create uwsgi user with home directory and nologin shell
RUN useradd -m -d /usr/src/app -s /usr/sbin/nologin uwsgi \
    && chown -R uwsgi:uwsgi /usr/src/app

USER uwsgi

EXPOSE 8000
VOLUME [ "/usr/src/app/data" ]

CMD ["uwsgi", "--ini", "uwsgi.ini"]
