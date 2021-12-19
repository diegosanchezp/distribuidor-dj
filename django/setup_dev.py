"""
Script to automatically setup django development environment
"""

import os
import subprocess as sp
from pathlib import Path

import environ

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "distribuidor_dj.settings.development"
)


# TODO: move this to an utils dir


def read_env(BASE_DIR):
    """
    Read environment variables
    """

    ENV_DIR = BASE_DIR / ".envs" / "local"
    env = environ.Env()
    env.read_env(str(ENV_DIR / "postgres"))
    env.read_env(str(ENV_DIR / "django"))
    return env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent  # Directory of this file

env = read_env(BASE_DIR)

# Check that env is activated by importing django
try:
    import django  # noqa: F401
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc

# Maybe refactor later using psycopg2 ?
# Create database and database user
try:
    sp.run(
        [
            "psql",
            "-h",
            env("POSTGRES_HOST"),
            "-U",
            "postgres",  # noqa: E501
            "-c",
            f"CREATE DATABASE {env('POSTGRES_DB_NAME')};",  # noqa: E501
            "-c",
            f"CREATE USER {env('POSTGRES_USER')} WITH PASSWORD '${env('POSTGRES_PASSWORD')}';",  # noqa: E501
            "-c",
            f"ALTER ROLE {env('POSTGRES_USER')} set client_encoding to 'utf8';",  # noqa: E501
            "-c",
            f"ALTER ROLE {env('POSTGRES_USER')} SET default_transaction_isolation TO 'read committed';",  # noqa: E501
            "-c",
            f"ALTER ROLE {env('POSTGRES_USER')} SET timezone TO 'America/Caracas';",  # noqa: E501
            "-c",
            f"GRANT ALL PRIVILEGES ON DATABASE {env('POSTGRES_DB_NAME')} TO {env('POSTGRES_USER')};",  # noqa: E501
        ],
        check=True,
    )
except sp.CalledProcessError as e:
    # Better message ?
    raise e

MANAGE = str(BASE_DIR / "manage.py")
# Install django-tailwind nodejs dependencies
sp.run(["python", MANAGE, "tailwind", "install"])

# Install git hooks
print("Installing git hooks")
sp.run(["pre-commit", "install"])

# Apply migrations
sp.run(["python", MANAGE, "migrate"])

print("createsuperuser (asking for password)")

sp.run(
    [
        "python",
        MANAGE,
        "createsuperuser",
        "--username",
        env("SUPER_USER"),
        "--email",
        f"{env('SUPER_USER')}@dev.com",
    ]
)
