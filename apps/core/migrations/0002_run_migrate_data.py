from django.db import migrations


class Migration(migrations.Migration):
    # This migration REPLACES the orphaned records that exist in the
    # production django_migrations table but were removed from the repo.
    # Django's graph loader uses `replaces` to delete orphaned DB rows
    # at load time, resolving ConflictingMigrationHistory errors.
    replaces = [
        ("core", "0002_run_migrate_data"),
        ("core", "0002_sync_pages"),
        ("core", "0002_refresh_home"),
        ("core", "0002_cleanup"),
        ("core", "0002_sync_fix"),
    ]

    dependencies = [
        ("core", "0001_seed_content"),
    ]

    operations = []
