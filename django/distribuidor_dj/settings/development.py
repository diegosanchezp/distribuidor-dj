"""
Django settings for distribuidor_dj project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os

from .base import *  # noqa

# read environment files
ENV_DIR = BASE_DIR / ".envs" / "local"  # noqa F405
env.read_env(str(ENV_DIR / "django"))  # noqa F405
env.read_env(str(ENV_DIR / "postgres"))  # noqa F405

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")  # noqa F405

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB_NAME"),  # noqa F405
        "USER": env("POSTGRES_USER"),  # noqa F405
        "PASSWORD": env("POSTGRES_PASSWORD"),  # noqa F405
        "HOST": env("POSTGRES_HOST"),  # noqa F405
        "PORT": env("POSTGRES_PORT"),  # noqa F405
        "ATOMIC_REQUESTS": True,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = str(BASE_DIR / "staticfiles")  # noqa F405
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(BASE_DIR / "static")]  # noqa F405

# Media Files
# https://overiq.com/django-1-10/handling-media-files-in-django/
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa F405
MEDIA_URL = "/media/"
