# Seed site content from the idempotent migrate_data command.
# CodeRed Cloud runs `manage.py migrate` on deploy (no SSH / no postdeploy hooks),
# so this data migration is the only reliable way to populate the site on first boot.

from django.db import migrations


def seed_content(apps, schema_editor):
    import os
    import sys
    # Skip seeding when running tests: the DB is populated by test setUp, and
    # seeding here would create duplicate pages (path collisions).
    if "test" in sys.argv:
        return
    from django.db import connection
    from django.core.management import call_command
    try:
        call_command("migrate_data")
    except Exception as e:
        print(f"[seed_content] migrate_data failed: {type(e).__name__}: {e}", file=sys.stderr)
    # Optionally create a superuser from env (set in CodeRed dashboard if desired).
    su_name = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    su_pass = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    if su_name and su_pass:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username=su_name).exists():
            User.objects.create_superuser(su_name, os.environ.get("DJANGO_SUPERUSER_EMAIL", ""), su_pass)
            print(f"[seed_content] created superuser {su_name}", file=sys.stderr)


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0004_alter_codexpage_articles"),
        ("discussions", "0001_initial"),
        ("home", "0003_searchpage"),
        ("institute", "0002_alter_subjectpage_curriculum"),
        ("news", "0002_alter_newspage_body"),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_content, migrations.RunPython.noop),
    ]
