import os

# general settings
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# apps in project
INSTALLED_APPS = [
    'ads',
    'sekizai',
    'reset_migrations',
    'ckeditor',
    'ckeditor_uploader',
    'damzi.apps.DamziConfig',
    'kitchen.apps.KitchenConfig',
    'library.apps.LibraryConfig',
    'accounts.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
]

# general middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'damzinium.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'damzinium.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'
AUTH_PROFILE_MODULE = 'accounts.Profile'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/accounts/login'

# ckeditor configuration
CKEDITOR_UPLOAD_PATH = 'uploads'
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}
X_FRAME_OPTIONS = 'SAMEORIGIN'

ADS_ZONES = {
    'header': {
        'name': ('Header'),
        'ad_size': {
            'xs': '720x1280',
            'sm': '720x1280',
            'md': '800x90',
            'lg': '800x90'
        },
    },

    'content': {
        'name': ('Content'),
        'ad_size': {
            'xs': '720x1280',
            'sm': '720x1280',
            'md': '800x90',
            'lg': '800x90'
        },
    },

    'sidebar': {
        'name': ('Sidebar'),
        'ad_size': {
            'xs': '720x1280',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90'
        },
    },
}
