from django.db import migrations


class Migration(migrations.Migration):
    # Replaces all orphaned core migration records that exist in the
    # production django_migrations table but have no corresponding
    # migration file in this repository.  Django's graph loader will
    # silently drop the orphaned DB rows when it sees this `replaces`.
    replaces = [
        ("core", "0002_run_migrate_data"),
        ("core", "0002_sync_pages"),
        ("core", "0002_refresh_home"),
        ("core", "0002_cleanup"),
        ("core", "0002_sync_fix"),
        ("core", "0003_sync_fix"),
    ]

    dependencies = [("core", "0001_seed_content")]
    operations = []
