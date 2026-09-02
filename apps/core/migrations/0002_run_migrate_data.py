from django.db import migrations


class Migration(migrations.Migration):

    # This migration replaces orphaned records that exist in the production
    # database but were removed from the repository in earlier refactors.
    # Django's `replaces` mechanism automatically marks those DB records
    # as applied (or removes them) when this migration is applied, resolving
    # the "Conflicting migrations detected" / MultipleLeafNodes error.
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
