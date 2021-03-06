import os

here = lambda path: os.path.join(os.path.realpath(os.path.dirname(__file__)), path)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ENV = os.environ.get('JUNIOR_ENV', 'prod')

ADMINS = (
    ('Alex Michael', 'alex@projectcel.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': here('../juniordb'),
    }
}

ALLOWED_HOSTS = [
    '.hackcyprus.com'
]

TIME_ZONE = 'Europe/Athens'

LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = '/var/junior/media/'
MEDIA_URL = ''

STATIC_ROOT = here('../static-collected')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    here('../static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'secret'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'junior.context_processors.expose_settings',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'teams.middleware.TeamExtractionMiddleware'
)

ROOT_URLCONF = 'junior.urls'

WSGI_APPLICATION = 'junior.wsgi.application'

TEMPLATE_DIRS = (
    here('../templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # third-party apps
    'south',
    'devserver',

    # project apps
    'teams',
    'game'
)

PUSHER_APP_ID = '53340'
PUSHER_KEY = 'pusher-key'
PUSHER_SECRET = 'pusher-secret'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if ENV == 'dev':
    from dev_settings import *

try:
    from secrets import *
except ImportError, exp:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
except:
    pass

try:
    MIDDLEWARE_CLASSES += LOCAL_MIDDLEWARE_CLASSES
except:
    pass

# initialize pusher
from lib import sync
sync.connect()
