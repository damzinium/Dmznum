import django_heroku

from .base import *

SECRET_KEY = '1@!@#$kjsk#$%8923@kalkj,2TThSk@344#!@3$5#@()*(*&(*('

DEBUG = True

ALLOWED_HOSTS = []

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())
