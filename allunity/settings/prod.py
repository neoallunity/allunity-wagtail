"""Production settings for CodeRed Cloud deployment.

CodeRed Cloud injects the following environment variables at runtime:
- SECRET_KEY
- ALLOWED_HOSTS (comma-separated)
- DATABASE_URL (e.g. mysql://user:pass@host:3306/db)
- REDIS_URL (optional)
"""
from .base import *  # noqa
import os

SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "allunity.codered.cloud").split(",")

# Database (CodeRed provides DATABASE_URL)
_database_url = os.environ.get("DATABASE_URL")
if _database_url:
    try:
        import dj_database_url
        DATABASES = {"default": dj_database_url.parse(_database_url)}
    except Exception:
        pass

# Security (served behind CodeRed's TLS-terminating proxy)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 63072000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Cache (optional Redis)
_redis_url = os.environ.get("REDIS_URL")
if _redis_url:
    try:
        import django_redis  # noqa
        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": _redis_url,
                "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            }
        }
    except Exception:
        pass
