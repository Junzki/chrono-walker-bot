FROM docker.io/python:3.13-bullseye

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

RUN --mount=type=secret,id=r2_access_key_id,env=R2_ACCESS_KEY_ID \
    --mount=type=secret,id=r2_secret_access_key,env=R2_SECRET_ACCESS_KEY \
    --mount=type=secret,id=r2_bucket_name,env=R2_BUCKET_NAME \
    --mount=type=secret,id=r2_account_id,env=R2_ACCOUNT_ID \
    python manage.py collectstatic --noinput

# Create uwsgi user with home directory and nologin shell
RUN useradd -m -d /usr/src/app -s /usr/sbin/nologin uwsgi \
    && chown -R uwsgi:uwsgi /usr/src/app

USER uwsgi

EXPOSE 8000
VOLUME [ "/usr/src/app/data" ]

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
