import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "allunity.settings.prod")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# On first boot (fresh database) seed content from the idempotent migration command.
import sys
try:
    from wagtail.models import Page
    if not Page.objects.filter(slug="home").exists():
        from django.core.management import call_command
        print("[wsgi] seeding content via migrate_data...", file=sys.stderr)
        call_command("migrate_data")
        print("[wsgi] migrate_data done", file=sys.stderr)
    else:
        print("[wsgi] home page already exists, skip seeding", file=sys.stderr)
except Exception as e:
    print(f"[wsgi] seed error: {type(e).__name__}: {e}", file=sys.stderr)
