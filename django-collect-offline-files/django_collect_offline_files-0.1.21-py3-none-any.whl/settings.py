"""
Django settings for django_collect_offline_files project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import sys
import os

from django.utils import timezone
from pathlib import PurePath

from .loggers import LOGGING

LOGGING = LOGGING

APP_NAME = 'django_collect_offline_files'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_DIR = os.path.join(BASE_DIR, 'etc')
SITE_ID = 40
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b78lzww*t&x&suam82%0#d3s339c5ufet$j^x#x+59fb)0p6fv'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'django_crypto_fields.apps.AppConfig',
    'edc_base.apps.AppConfig',
    'edc_protocol.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'django_collect_offline.apps.AppConfig',
    'django_collect_offline_files.apps.AppConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_collect_offline_files.urls'

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

WSGI_APPLICATION = 'django_collect_offline_files.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': os.path.join(ETC_DIR, 'default.cnf'),
#         },
#     },
#     'client': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': os.path.join(ETC_DIR, 'client.cnf'),
#         },
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {'timeout': 20}
    },
    # required for tests when acting as a server but not attempting to
    # deserialize
    'server': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # required for tests when acting as a client
    'client': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {'timeout': 20}
    },
    'test_server': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

GIT_DIR = str(PurePath(BASE_DIR).parent)
# KEY_PATH = os.path.join(BASE_DIR, 'crypto_fields')
EDC_CRYPTO_FIELDS_CLIENT_USING = 'client'
SHOW_CRYPTO_FORM_DATA = True
STUDY_OPEN_DATETIME = timezone.datetime(2016, 1, 18)
LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)
CURRENT_MAP_AREA = None

DEVICE_ID = '15'
SERVER_DEVICE_ID_LIST = ['99']

APP_LABEL = 'django_collect_offline_files'
COMMUNITY = ''

DJANGO_COLLECT_OFFLINE_SERVER_IP = None
DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST = None
DJANGO_COLLECT_OFFLINE_FILES_USER = 'django'
DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME = '/Volumes/BCPP'

if 'test' in sys.argv:

    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
