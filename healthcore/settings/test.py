"""
Django settings for the test environment (e.g., CI).

This file inherits from base.py and is optimized for running tests.
It expects service configurations (database, cache) to be provided
by the CI runner's environment variables.
"""

from .base import *  # noqa: F401, F403

# Use a fast, insecure password hasher for tests to speed up user creation.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Use an in-memory email backend for tests to avoid sending real emails.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
