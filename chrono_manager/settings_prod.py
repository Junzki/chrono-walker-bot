# -*- coding: utf-8 -*-

import os
from decouple import config

from .settings import *

DEBUG = config('debug', default=False, cast=bool)
URL_DEBUG = config('url_debug', default=False, cast=bool)

ALLOWED_HOSTS = [
    '*'
]

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',
    }
}

try:
    CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(",")
except AttributeError as e:
    pass

STATIC_URL = 'https://static.lgtkom.dev/'
MEDIA_URL = 'https://static.lgtkom.dev/media/'
