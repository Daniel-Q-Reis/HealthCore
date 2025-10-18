"""
Django settings for the test environment (e.g., CI).

This file inherits from base.py and is optimized for running tests.
It expects service configurations (database, cache) to be provided
by the CI runner's environment variables.
"""

from .base import *  # noqa: F401, F403

# Explicitly add health check apps for the test environment.
# This ensures they are always available for testing the health endpoints,
# regardless of the conditional logic in base.py.
try:
    import health_check  # noqa: F401

    INSTALLED_APPS.extend(  # noqa: F405
        ["health_check", "health_check.db", "health_check.cache"]
    )
except ImportError:
    pass

# Use a fast, insecure password hasher for tests to speed up user creation.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Use an in-memory email backend for tests to avoid sending real emails.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
