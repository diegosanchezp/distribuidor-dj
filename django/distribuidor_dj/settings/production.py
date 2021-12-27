import django_heroku

from .base import *  # noqa

# Activate Django-Heroku. This line should always be last
# beacuse the locals function reads all of the variables
# defined in this file

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")  # noqa F405
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

django_heroku.settings(locals())
