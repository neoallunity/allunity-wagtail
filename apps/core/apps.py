import sys
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        # Only connect post_migrate in production; during tests the
        # 0001_seed_content migration (with its own guard) seeds content
        # and the migrate_data command is called from the migration directly.
        if "test" not in sys.argv:
            post_migrate.connect(self._sync_content, sender=self)

    def _sync_content(self, sender, **kwargs):
        from django.core.management import call_command
        try:
            call_command("migrate_data", verbosity=0)
        except Exception:
            pass