"""
Django settings for Sprint project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


HOST = os.getenv("HOST", "77.246.159.65")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "-w#*mn6*fa8a=(-c0@klx&$vl%hpiy&l(u*3%0a#2)wdt##(z2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('debug', 'true') == 'true'


ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Main.apps.MainConfig",
    "Checker.apps.CheckerConfig",
    "Messaging.apps.MessagingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "Sprint.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "Main.context_processors.attributes",
            ],
        },
    },
]

WSGI_APPLICATION = "Sprint.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "sprint",
        "USER": "postgres",
        "PASSWORD": os.getenv("DB_PASSWORD", "password"),
        "HOST": HOST,
        "PORT": 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

_ = lambda s: s

LANGUAGES = (("en", _("English")), ("ru", _("Russian")))

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# STATIC_ROOT = os.path.join(BASE_DIR, "static")
DATA_ROOT = os.path.join(BASE_DIR, "data")
EXTRA_FILES_ROOT = os.path.join(BASE_DIR, "extra_files")
SOLUTIONS_ROOT_EXTERNAL = os.getenv("SOLUTIONS_ROOT_EXTERNAL", os.path.join(DATA_ROOT, "solutions"))
for root in DATA_ROOT, EXTRA_FILES_ROOT:
    if not os.path.exists(root):
        os.mkdir(root)

SOLUTIONS_ROOT = os.path.join(DATA_ROOT, "solutions")

RABBIT_HOST = HOST
RABBIT_PORT = 5672

FS_HOST = "http://" + HOST
FS_PORT = 5555

# Authentication backends
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

CONSTS = {
    "online_status": "Online",
    "in_queue_status": "In queue",
    "testing_status": "Testing",
    "ok_status": "OK",
}

if not DEBUG:
    sentry_sdk.init(
        dsn="https://bd56bba96dbe4017a792810a8be6cfc1@o1155463.ingest.sentry.io/6235928",
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
