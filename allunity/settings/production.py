from .base import *  # noqa
DEBUG = False
import os
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "allunity.ru,www.allunity.ru").split(",")
SECRET_KEY = os.environ["SECRET_KEY"]  # required in production; fail fast if absent
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 63072000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Use Postgres when DATABASE_URL is provided (docker-compose); otherwise keep base SQLite.
_database_url = os.environ.get("DATABASE_URL")
if _database_url:
    try:
        import dj_database_url
        DATABASES = {"default": dj_database_url.parse(_database_url)}
    except Exception:
        pass

try:
    import importlib.util as _ilu
    if _ilu.find_spec("compressor"):
        COMPRESS_ENABLED = True
    if _ilu.find_spec("django_redis"):
        CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache",
                              "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1"),
                              "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}
except Exception:
    pass
