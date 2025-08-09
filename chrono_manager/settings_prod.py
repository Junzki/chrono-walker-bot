# -*- coding: utf-8 -*-

import os

from .settings import *

DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY_TO_REPLACE")

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
