from django.apps import AppConfig
from django.db.models.signals import post_migrate


def ensure_content_pages(sender, **kwargs):
    import sys
    if "test" in sys.argv:
        return
    
    from django.core.management import call_command
    try:
        call_command("migrate_data", verbosity=0)
    except Exception as e:
        print(f"[apps.core] migrate_data failed: {e}", file=sys.stderr)


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        post_migrate.connect(ensure_content_pages, sender=self)