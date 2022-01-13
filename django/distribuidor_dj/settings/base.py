from pathlib import Path

import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ---- Our apps ----
    "distribuidor_dj.apps.api.apps.ApiConfig",
    "distribuidor_dj.apps.home.apps.HomeConfig",
    "distribuidor_dj.apps.state.apps.StateConfig",
    "distribuidor_dj.apps.invoice.apps.InvoiceConfig",
    "distribuidor_dj.apps.shipment.apps.ShipmentConfig",
    "distribuidor_dj.apps.customer.apps.CustomerConfig",
    # ---- Third party ----
    # API REST
    "rest_framework",
    "drf_spectacular",
    # JS
    "django_htmx",
    "django_node_assets",
    # CSS
    "tailwind",
    "distribuidor_dj.apps.tailwind_theme.apps.Tailwind_themeConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "distribuidor_dj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "distribuidor_dj.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_node_assets.finders.ManifestNodeModulesFinder",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = str(BASE_DIR / "staticfiles")  # noqa F405
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Distribuidor API",
    "DESCRIPTION": "Comercio electrónico 2-2021, Distribuidor API",
    "VERSION": "1.0.0",
    # OTHER SETTINGS
}

# django-tailwind config
TAILWIND_THEME = "tailwind_theme"
TAILWIND_APP_NAME = f"distribuidor_dj.apps.{TAILWIND_THEME}"
INTERNAL_IPS = [
    "127.0.0.1",
]

# django-node-assets config
STATIC_SRC = (
    BASE_DIR / "distribuidor_dj" / "apps" / TAILWIND_THEME / "static_src"
)
NODE_PACKAGE_JSON = str(STATIC_SRC / "package.json")
NODE_MODULES_ROOT = str(STATIC_SRC / "node_modules")
