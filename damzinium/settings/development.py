from .base import *

SECRET_KEY = '!@#$i93249!#jaoi1#@$1iojlkjo1@#$1o3i@#'

# allow for detailed errors to be shown
DEBUG = True

# developent allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', ]

# development database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')