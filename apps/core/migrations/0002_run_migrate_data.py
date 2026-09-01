from django.db import migrations


def run_migrate_data(apps, schema_editor):
    from django.core.management import call_command
    try:
        call_command("migrate_data", verbosity=0)
    except Exception as e:
        print(f"[0002_run_migrate_data] failed: {e}")


class Migration(migrations.Migration):
    dependencies = [("core", "0001_seed_content")]

    operations = [
        migrations.RunPython(run_migrate_data, migrations.RunPython.noop),
    ]