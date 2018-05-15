"""
For development environment use "--settings=meisr.local_settings" flag
"""

from .settings import *

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = '=b&ac*07cl(wdi-yp(7p=s8@hnls&@p=l-7=+#obpaq#!9jc%i'

ALLOWED_HOSTS = ['localhost']

SECURE_SSL_REDIRECT = False

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
