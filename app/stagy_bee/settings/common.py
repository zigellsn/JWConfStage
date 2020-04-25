#  Copyright 2019 Simon Zigelli
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import asyncio
import json
import os
import sys
from pathlib import Path

from decouple import config, Csv
from django.utils.translation import gettext_lazy as _

# Needed for now when using Python 3.8 on Windows
if sys.platform == 'win32' and sys.version_info.major == 3 and sys.version_info.minor == 8:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

BASE_DIR = PROJECT_PACKAGE.parent

try:
    with open(f"{PROJECT_PACKAGE}/regex.json", encoding="utf-8") as json_file:
        WB_LANGUAGE_SWITCHER = json.load(json_file)
except FileNotFoundError:
    WB_LANGUAGE_SWITCHER = {}

VERSION = "0.2.0-alpha"

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

# Application definition

INSTALLED_APPS = [
    'channels',
    'guardian',
    'stage',
    'receiver',
    'console',
    'picker.apps.PickerConfig',
    'audit.apps.AuditConfig',
    'stopwatch.apps.StopwatchConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'stagy_bee.urls'
LOGIN_REDIRECT_URL = '/console/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_PORT = config("EMAIL_PORT", default="25")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'stagy_bee.wsgi.application'

ASGI_APPLICATION = "stagy_bee.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(config("REDIS_HOST", default="localhost"), config("REDIS_PORT", default=6379, cast=int))],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": config("SQL_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("SQL_DATABASE", default=os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": config("SQL_USER", default="user"),
        "PASSWORD": config("SQL_PASSWORD", default="password"),
        "HOST": config("SQL_HOST", default="localhost"),
        "PORT": config("SQL_PORT", default="5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGES = config('LANGUAGES', default="de:German,en:English",
                   cast=Csv(cast=lambda s: (s.split(':')[0], _(s.split(':')[1])), delimiter=',', strip=' %*'))

LANGUAGE_CODE = 'de'

LOCALE_PATHS = (
    str(PROJECT_PACKAGE.joinpath('locale')),
)

TIME_ZONE = 'CET'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/assets')
STATICFILES_DIRS = [str(PROJECT_PACKAGE.joinpath('static'))]
