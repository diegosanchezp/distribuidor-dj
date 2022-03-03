import dj_database_url
import django_heroku

from .base import *  # noqa

# Activate Django-Heroku. This line should always be last
# beacuse the locals function reads all of the variables
# defined in this file

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")  # noqa F405

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}  # noqa F405

CSRF_TRUSTED_ORIGINS = [
    "https://distribuidor-dj.herokuapp.com",
    "https://*.herokuapp.com",
]

# Danger
ALLOWED_HOSTS = ["*"]
STATICFILES_STORAGE = "distribuidor_dj.storage.WhiteNoiseStaticFilesStorage"

# https://stackoverflow.com/questions/70508568/django-csrf-trusted-origins-not-working-as-expected


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

django_heroku.settings(
    locals(),
    databases=False,
    test_runner=False,
    staticfiles=False,
    logging=False,
)
