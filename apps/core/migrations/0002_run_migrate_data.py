import sys
from django.db import migrations, connection


def clear_orphaned_migrations(apps, schema_editor):
    """Remove stale rows from django_migrations that have no file.

    CodeRed Cloud's `cr deploy` runs `manage.py migrate`.  The DB may
    contain rows for migration files that were removed from the repo
    during earlier refactors; Django's migrator refuses to continue
    until those rows are gone.
    """
    with connection.cursor() as cur:
        cur.execute(
            "DELETE FROM django_migrations "
            "WHERE app = 'core' AND name IN ("
            "'0002_sync_pages', '0002_refresh_home', "
            "'0002_cleanup', '0002_sync_fix', '0003_sync_fix')"
        )
        print(
            f"[0002_run_migrate_data] cleared "
            f"{cur.rowcount} orphaned core migration rows",
            file=sys.stderr,
        )


def seed_and_sync(apps, schema_editor):
    """Seed content from allunity.ru on every deploy."""
    if "test" in sys.argv:
        return
    from django.core.management import call_command
    try:
        call_command("migrate_data", verbosity=0)
    except Exception as e:
        print(f"[0002_run_migrate_data] failed: {e}", file=sys.stderr)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_seed_content"),
        ("home", "0003_searchpage"),
    ]
    operations = [
        migrations.RunPython(clear_orphaned_migrations, migrations.RunPython.noop),
        migrations.RunPython(seed_and_sync, migrations.RunPython.noop),
    ]