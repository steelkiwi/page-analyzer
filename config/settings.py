# -*- coding: utf-8 -*-
import sys
import logging

import environ
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from corsheaders.defaults import default_headers


# page_analyzer/config/settings.py - 2 = page_analyzer/
ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path('page_analyzer')
sys.path.append('page_analyzer/apps')

# Environment
# https://django-environ.readthedocs.io/en/latest/#how-to-use
# ------------------------------------------------------------------------------
# Default values and casting
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, ''),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    # Static/Media
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR('staticfiles'))),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR('media'))),
    # Database
    POSTGRES_HOST=(str, 'db'),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, ''),
    POSTGRES_USER=(str, ''),
    POSTGRES_PASSWORD=(str, ''),
    # Email
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, 'consolemail://'),
    DJANGO_EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'admin@example.com'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost.com'),
    # Celery
    DJANGO_CELERY_BROKER_URL=(str, 'redis://redis:6379/0'),
    DJANGO_CELERY_BACKEND=(str, 'redis://redis:6379/0'),
    DJANGO_CELERY_ALWAYS_EAGER=(bool, False),
    # Debug
    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_TEST_RUN=(bool, False),
    DJANGO_DEBUG_SQL=(bool, False),
    DJANGO_DEBUG_SQL_COLOR=(bool, False),
    # Third party API
    # AWS
    DJANGO_AWS_ACCESS_KEY_ID=(str, ''),
    DJANGO_AWS_SECRET_ACCESS_KEY=(str, ''),
    DJANGO_AWS_STORAGE_BUCKET_NAME=(str, ''),
    DJANGO_AWS_S3_CUSTOM_DOMAIN=(str, ''),
    # Sentry
    DJANGO_SENTRY_DSN=(str, ''),
    DJANGO_SENTRY_LOG_LEVEL=(int, logging.INFO),
    # CORS
    DJANGO_CORS_ORIGIN_WHITELIST=(list, []),
    DJANGO_CORS_ALLOW_HEADERS=(tuple, ()),
    # CUSTOM
    DJANGO_FRONTEND_EMAIL_CONFIRMATION_URL=(str, ''),
    DJANGO_FRONTEND_PASSWORD_RESET_URL=(str, ''),
)

# Django Core
# https://docs.djangoproject.com/en/2.2/ref/settings/#core-settings
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG")
SECRET_KEY = env('DJANGO_SECRET_KEY')
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
ADMINS = tuple([
    tuple(admins.split(':'))
    for admins in env.list('DJANGO_ADMINS')
])
MANAGERS = ADMINS
ADMIN_URL = 'admin/'
ADMIN_SITE_TITLE = 'page-analyzer'
ADMIN_SITE_HEADER = 'page-analyzer'
TIME_ZONE = 'UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DATA_UPLOAD_MAX_MEMORY_SIZE = 20_971_520  # 20MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20_971_520  # 20MB

# Django Sites
# https://docs.djangoproject.com/en/2.2/ref/settings/#sites
# ------------------------------------------------------------------------------
SITE_ID = 1

# Django Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# Django Applications
# https://docs.djangoproject.com/en/2.2/ref/settings/#installed-apps
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ckeditor',
    'corsheaders',
    'rest_auth',
    'rest_auth.registration',
    'imagekit'
)
LOCAL_APPS = (
    'users.apps.UsersAppConfig',
    'flatpages.apps.FlatpagesConfig',
    'files.apps.FilesConfig',
    'analyzer.apps.AnalyzerConfig'
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Django Middlewares
# https://docs.djangoproject.com/en/2.2/ref/settings/#middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Django Email Server
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-backend
# ------------------------------------------------------------------------------
EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')
EMAIL_BACKEND = EMAIL_URL['EMAIL_BACKEND']
EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER', '')
EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT', '')
EMAIL_USE_SSL = 'EMAIL_USE_SSL' in EMAIL_URL
EMAIL_USE_TLS = 'EMAIL_USE_TLS' in EMAIL_URL
EMAIL_FILE_PATH = EMAIL_URL.get('EMAIL_FILE_PATH', '')
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL')

# Django Templates
# https://docs.djangoproject.com/en/2.2/ref/settings/#templates
# ------------------------------------------------------------------------------
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        str(APPS_DIR.path('templates')),
    ],
    'OPTIONS': {
        'debug': DEBUG,
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# Django Logging
# https://docs.djangoproject.com/en/2.2/ref/settings/#logging
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# Django Static Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#static-files
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT')
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Django Cache
# https://docs.djangoproject.com/en/3.0/topics/cache/
# ------------------------------------------------------------------------------
# Analysis TTL cache constance in seconds
ANALYSIS_CACHE_TTL = 60*60*24
ANALYSIS_CACHE = 'default'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'analysis_cache_table',
        'TIMEOUT': ANALYSIS_CACHE_TTL,

    }
}

# Django Media Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#media-root
# ------------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

# Django Auth
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'api:users:auth:login'
LOGIN_REDIRECT_URL = '/'

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_EMAIL_FIELD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False

# django-rest-auth
# https://django-rest-auth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
LOGOUT_ON_PASSWORD_CHANGE = False
OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'users.serializers.TokenSerializer',
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
    'PASSWORD_RESET_SERIALIZER': 'users.serializers.PasswordResetSerializer'
}

# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/
# ------------------------------------------------------------------------------
PAGE_SIZE = 20
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': PAGE_SIZE,
}
ENABLE_BROWSABLE_API_RENDERER = env.bool('DRF_ENABLE_BROWSABLE_API_RENDERER', False)
if ENABLE_BROWSABLE_API_RENDERER:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

# django-storages: Amazon S3
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = env('DJANGO_AWS_S3_CUSTOM_DOMAIN')
AWS_S3_MAX_MEMORY_SIZE = 10  # roll over to temporary file on disk if over limit
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')

# Celery
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = env('DJANGO_CELERY_BROKER_URL')
CELERY_BACKEND = env('DJANGO_CELERY_BACKEND')
if env.bool('DJANGO_TEST_RUN') or any('pytest' in arg for arg in sys.argv):
    CELERY_ALWAYS_EAGER = True
else:
    CELERY_ALWAYS_EAGER = env.bool('DJANGO_CELERY_ALWAYS_EAGER')

# Sentry SDK
# https://docs.sentry.io/platforms/python/logging/
# https://docs.sentry.io/platforms/python/django/
# https://docs.sentry.io/platforms/python/celery/
# ------------------------------------------------------------------------------
SENTRY_DSN = env('DJANGO_SENTRY_DSN')
SENTRY_LOG_LEVEL = env('DJANGO_SENTRY_LOG_LEVEL')
LOGGING['loggers']['sentry_sdk'] = {
    'level': 'ERROR',
    'handlers': ['console'],
    'propagate': False
}
sentry_logging = LoggingIntegration(level=SENTRY_LOG_LEVEL, event_level=None)
sentry_sdk.init(dsn=SENTRY_DSN, integrations=[sentry_logging, DjangoIntegration(), CeleryIntegration()])

# Django Debug Toolbar
# ------------------------------------------------------------------------------
USE_DEBUG_TOOLBAR = env.bool('DJANGO_USE_DEBUG_TOOLBAR')
if USE_DEBUG_TOOLBAR:
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', '10.0.2.2')
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

# django-sqlformatter
# https://github.com/gabrielhora/django_sqlformatter
# http://pygments.org/docs/styles/#getting-a-list-of-available-styles
# ------------------------------------------------------------------------------
SQL_FORMATTER_STYLE = env.str('DJANGO_DEBUG_SQL_FORMATTER_STYLE', default='default')
if env.bool('DJANGO_DEBUG_SQL', default=False):
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'propagate': False,
        'level': 'DEBUG',
    }
if env.bool('DJANGO_DEBUG_SQL_COLOR', default=False):
    LOGGING['handlers']['console']['formatter'] = 'sql'
    LOGGING['formatters']['sql'] = {
        '()': 'common.sqlformatter.SqlFormatter',
        'format': '%(levelname)s %(message)s',
    }

# Django CORS
# https://github.com/adamchainz/django-cors-headers#configuration
# ------------------------------------------------------------------------------
CORS_ORIGIN_WHITELIST = env.list('DJANGO_CORS_ORIGIN_WHITELIST')
CORS_ALLOW_HEADERS = default_headers + env.tuple('DJANGO_CORS_ALLOW_HEADERS')


# Imagekit settings
# https://github.com/matthewwithanm/django-imagekit
# ------------------------------------------------------------------------------
FILES_AVATAR_THUMB_SIZE = (600, 600)
FILES_AVATAR_THUMB_QUALITY = 60
FILES_AVATAR_EXTENSION = "JPEG"
IMAGEKIT_DEFAULT_FILE_STORAGE = 'files.storages.ThumbnailS3Boto3Storage'
IMAGEKIT_CACHEFILE_DIR = ''

# Custom settings
# ------------------------------------------------------------------------------
DJANGO_FRONTEND_EMAIL_CONFIRMATION_URL = env.str('DJANGO_FRONTEND_EMAIL_CONFIRMATION_URL')
DJANGO_FRONTEND_PASSWORD_RESET_URL = env.str('DJANGO_FRONTEND_PASSWORD_RESET_URL')
