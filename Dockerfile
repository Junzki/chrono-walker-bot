FROM docker.io/python:3.13-bullseye as build

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends firefox-esr build-essential libpq-dev && \
    apt-get clean && \
    python -m pip install -U pip && \
    pip install -r ./requirements.txt && \
    pip install uWSGI && \
    bash ./setup.sh

RUN --mount=type=secret,id=r2_access_key_id \
    --mount=type=secret,id=r2_secret_access_key \
    --mount=type=secret,id=r2_bucket_name \
    --mount=type=secret,id=r2_account_id \
    export R2_ACCESS_KEY_ID=$(cat /run/secrets/r2_access_key_id) && \
    export R2_SECRET_ACCESS_KEY=$(cat /run/secrets/r2_secret_access_key) && \
    export R2_BUCKET_NAME=$(cat /run/secrets/r2_bucket_name) && \
    export R2_ACCOUNT_ID=$(cat /run/secrets/r2_account_id) && \
    echo "Secrets loaded"

RUN python manage.py compilemessages && \
    python manage.py collectstatic --noinput

# -------------------------------------------------------------- #

FROM docker.io/python:3.13-bullseye

# Create uwsgi user with home directory and nologin shell
RUN useradd -m -d /usr/src/app -s /usr/sbin/nologin uwsgi \
    && chown -R uwsgi:uwsgi /usr/src/app

USER uwsgi

EXPOSE 8000
VOLUME [ "/usr/src/app/data" ]

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
