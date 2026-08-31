"""Production settings for CodeRed Cloud deployment.

CodeRed Cloud injects environment variables at runtime. The exact secret-key
variable name differs across CodeRed versions; we accept several common names
and fall back to a deterministic key derived from the site host so the app
boots even if the secret isn't injected.
"""
from .base import *  # noqa
import os

# PyMySQL is a pure-Python MySQL driver (no system libmysqlclient needed).
# Django's MySQL backend expects the `MySQLdb` module; shim it.
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    pass

_SECRET_CANDIDATES = ["SECRET_KEY", "DJANGO_SECRET_KEY", "CODERED_SECRET_KEY"]
_secret = None
for _name in _SECRET_CANDIDATES:
    _secret = os.environ.get(_name)
    if _secret:
        break
if not _secret:
    # Deterministic fallback so sessions survive restarts on the same host.
    _host = os.environ.get("ALLOWED_HOSTS", "allunity.codered.cloud")
    _secret = "cr-" + "".join(ch for ch in _host if ch.isalnum()) + "-allunity-wagtail"
SECRET_KEY = _secret

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "allunity.codered.cloud").split(",")

# Database (CodeRed provides DATABASE_URL, e.g. mysql://...)
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
