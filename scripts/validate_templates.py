import os, sys, pathlib, django
from django.conf import settings
ROOT = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parents[1])
settings.configure(
    DEBUG=False, SECRET_KEY="validation",
    INSTALLED_APPS=[
        "django.contrib.contenttypes","django.contrib.auth","django.contrib.staticfiles",
        "wagtail","wagtail.images","wagtail.documents","wagtail.snippets","wagtail.users",
        "wagtail.admin","wagtail.contrib.forms","wagtail.contrib.redirects",
    ],
    TEMPLATES=[{
        "BACKEND":"django.template.backends.django.DjangoTemplates",
        "DIRS":[os.path.join(ROOT,"templates")],
        "APP_DIRS":True,
        "OPTIONS":{"builtins":[
            "django.templatetags.static",
            "wagtail.templatetags.wagtailcore_tags",
            "wagtail.images.templatetags.wagtailimages_tags",
        ],"libraries":{
            "static":"django.templatetags.static",
            "wagtailcore_tags":"wagtail.templatetags.wagtailcore_tags",
            "wagtailimages_tags":"wagtail.images.templatetags.wagtailimages_tags",
        }},
    }],
    DATABASES={}, STATIC_URL="/static/",
)
django.setup()
from django.template import engines
engine = engines["django"].engine
errors=[]
for path in sorted(pathlib.Path(ROOT,"templates").rglob("*.html")):
    try:
        engine.from_string(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append((str(path.relative_to(ROOT)),type(exc).__name__,str(exc)[:220]))
for e in errors: print(" | ".join(e))
print("TOTAL_ERRORS",len(errors))
