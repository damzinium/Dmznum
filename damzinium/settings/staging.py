import django_heroku

from .base import *

SECRET_KEY = '1@!@#$kjsk#$%8923@kalkj,2TThSk@344#!@3$5#@()*(*&(*('

DEBUG = True

ALLOWED_HOSTS = ['staging.damzinium.herokuapp.com', ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE += [
	'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())