FROM docker.io/python:3.13-bullseye

ARG PIP_INDEX_URL=""

WORKDIR /usr/src/app


# Create uwsgi user with home directory and nologin shell
RUN useradd -m -d /usr/src/app -s /usr/sbin/nologin uwsgi \
    && chown -R uwsgi:uwsgi /usr/src/app

USER uwsgi

COPY misc/sources.list /etc/apt/sources.list

COPY . .

# Set ENV PIP_INDEX_URL only if ARG is not empty
RUN if [ -n "$PIP_INDEX_URL" ]; then \
    echo "PIP_INDEX_URL=$PIP_INDEX_URL" >> /etc/environment; \
    export PIP_INDEX_URL="$PIP_INDEX_URL"; \
fi

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends firefox-esr && \
    apt-get clean && \
    pip install -U pip && \
    pip install -r ./requirements.txt && \
    pip install uWSGI && \
    bash ./setup.sh

EXPOSE 8000
VOLUME [ "/usr/src/app/data" ]

CMD ["uwsgi", "--ini", "uwsgi.ini"]
