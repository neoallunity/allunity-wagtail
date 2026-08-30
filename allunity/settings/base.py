import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key-change-in-production")
DEBUG = False

# DB: SQLite by default (works everywhere); Postgres when DATABASE_URL is set.
import json as _json
_db_env = os.environ.get("DATABASE_URL")
if _db_env:
    # minimal URL parse: postgres://user:pass@host:port/db
    import urllib.parse as _up
    _u = _up.urlparse(_db_env)
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _u.path.lstrip("/"),
        "USER": _u.username or os.environ.get("DATABASE_USER", "allunity_user"),
        "PASSWORD": _u.password or os.environ.get("DATABASE_PASSWORD", ""),
        "HOST": _u.hostname or os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": str(_u.port or "5432"),
    }}
else:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(PROJECT_DIR / "db.sqlite3"),
    }}

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]
WAGTAIL_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.table_block",
]
THIRD_PARTY_APPS = ["modelcluster", "taggit"]
LOCAL_APPS = [
    "apps.core",
    "apps.home",
    "apps.institute",
    "apps.news",
    "apps.projects",
    "apps.discussions",
    "apps.content",
]
INSTALLED_APPS = DJANGO_APPS + WAGTAIL_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "apps.core.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "allunity.urls"

# Static files finders: include compressor only if installed
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
try:
    import importlib.util as _ilu
    if _ilu.find_spec("compressor"):
        STATICFILES_FINDERS.append("compressor.finders.CompressorFinder")
except Exception:
    pass

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WAGTAIL_SITE_NAME = "AllUnity"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"
WAGTAIL_USER_EDIT_FORM = "wagtail.users.forms.UserEditForm"
WAGTAIL_USER_CREATION_FORM = "wagtail.users.forms.UserCreationForm"
WAGTAIL_USER_CUSTOM_FIELDS = ["first_name", "last_name"]
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

ALLOWED_HOSTS = []

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "{levelname} {message}", "style": "{"}},
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"]},
}
