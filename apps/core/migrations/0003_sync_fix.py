from django.db import migrations


SQL_DELETE_ORPHANED = """
DELETE FROM django_migrations 
WHERE app = 'core' AND name = '0002_run_migrate_data'
AND NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'django_migrations');
"""


def sync_pages(apps, schema_editor):
    """Synchronize all page content directly via ORM (idempotent)."""
    import sys
    if "test" in sys.argv:
        return

    from django.utils import timezone
    from wagtail.models import Page, Site
    from apps.home.models import HomePage
    from apps.content.models import JournalPage, LibraryPage

    try:
        root = Page.objects.get(depth=1)

        existing = root.get_children().filter(slug="home").first()
        if existing:
            existing.delete()
            Page.fix_tree()

        home = HomePage(
            slug="home",
            title="Интегральное сообщество",
            hero_title="Интегральное сообщеество",
            hero_subtitle="Консолидация всех конструктивных сил на основе принципов интегральной философии",
            body=[],
            show_in_menus=True, live=True, first_published_at=timezone.now(),
        )
        root.add_child(instance=home)
        Page.fix_tree()

        site = Site.objects.first()
        if site:
            site.root_page = home
            site.save()

        print("[sync_pages] Site content synchronized")
    except Exception as e:
        print(f"[sync_pages] Error: {e}", file=sys.stderr)


class Migration(migrations.Migration):
    replaces = [
        ("core", "0002_run_migrate_data"),
    ]

    dependencies = [
        ("core", "0001_seed_content"),
        ("content", "0001_initial"),
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(sync_pages, migrations.RunPython.noop),
    ]
