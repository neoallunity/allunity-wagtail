import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "allunity.settings.prod")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import sys as _sys
try:
    from wagtail.models import Page
    if not Page.objects.filter(slug="home").exists():
        from django.core.management import call_command
        print("[wsgi-root] seeding content via migrate_data...", file=_sys.stderr)
        call_command("migrate_data")
        print("[wsgi-root] migrate_data done", file=_sys.stderr)
except Exception as e:
    print(f"[wsgi-root] seed error: {type(e).__name__}: {e}", file=_sys.stderr)
