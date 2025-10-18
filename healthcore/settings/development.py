import os

from decouple import config

from .base import *  # noqa: F403

# SECURITY WARNING: keep the secret key used in production secret!
# In development, we can use a default value, but it must still come from environment variables
SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-development-key-for-local-use-only"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "healthcore_db"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Celery and Cache settings for development, using Docker service names as defaults
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://redis:6379/1"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React default port
    "http://127.0.0.1:3000",
]

# For development, you might want to allow all origins
# CORS_ALLOW_ALL_ORIGINS = True

# DRF Spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "HealthCore API",
    "DESCRIPTION": "HealthCore API** is a secure, scalable, and high-performance backend system for complete hospital operations management. This project serves as the technological backbone for managing patients, appointments, electronic health records, and administrative processes, built upon an enterprise-grade foundation.",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}
