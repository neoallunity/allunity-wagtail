# Seed site content from the idempotent migrate_data command.
# CodeRed Cloud runs `manage.py migrate` on deploy (no SSH / no postdeploy hooks),
# so this data migration is the only reliable way to populate the site on first boot.

from django.db import migrations


def seed_content(apps, schema_editor):
    import sys
    if "test" in sys.argv:
        return

    from django.core.management import call_command
    try:
        call_command("migrate_data")
    except Exception as e:
        # Never block a deploy on a seeding failure; operator can re-run manually.
        print(f"[seed_content] migrate_data failed: {type(e).__name__}: {e}", file=sys.stderr)


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(seed_content, migrations.RunPython.noop),
    ]