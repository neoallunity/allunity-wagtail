from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        post_migrate.connect(self._sync_content, sender=self)

    def _sync_content(self, sender, **kwargs):
        import sys
        if "test" in sys.argv:
            return

        from django.core.management import call_command
        try:
            call_command("migrate_data", verbosity=0)
        except Exception:
            pass