import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "allunity.settings.prod")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# On first boot (fresh database) seed content from the idempotent migration command.
# Runs once: guarded by the presence of a HomePage.
try:
    from wagtail.models import Page
    if not Page.objects.filter(slug="home").exists():
        from django.core.management import call_command
        call_command("migrate_data")
except Exception:
    # Never let content seeding break the app boot.
    pass
