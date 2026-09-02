from django.db import migrations


def sync_content(apps, schema_editor):
    """Synchronize all page content directly via ORM (idempotent)."""
    import sys
    if "test" in sys.argv:
        return

    from django.utils import timezone
    from wagtail.models import Page, Site
    from apps.home.models import HomePage
    from apps.content.models import JournalPage, LibraryPage
    import datetime

    try:
        root = Page.objects.get(depth=1)

        # Delete and recreate home
        existing = root.get_children().filter(slug="home").first()
        if existing:
            existing.delete()
            Page.fix_tree()

        home = HomePage(
            slug="home",
            title="Интегральное сообщество",
            hero_title="Интегральное сообщество",
            hero_subtitle="Консолидация всех конструктивных сил на основе принципов интегральной философии",
            body=[
                ("heading", "Манифест неовсеединства"),
                ("paragraph", "На пути к обществу развития. Философия неовсеединства формулирует принципы эволюции и синтеза на основе принципов всеединства."),
            ],
            show_in_menus=True, live=True, first_published_at=timezone.now(),
        )
        root.add_child(instance=home)
        Page.fix_tree()

        # Update site root
        site = Site.objects.first()
        if site:
            site.root_page = home
            site.save()

        # Ensure journal exists at root level
        journal = root.get_children().filter(slug="journal").first()
        if journal:
            journal.delete()
            Page.fix_tree()
        journal_page = JournalPage(
            slug="journal",
            title="Журнал «Интегральная философия»",
            volume="№ 15",
            live=True, show_in_menus=True, first_published_at=timezone.now(),
            description="<p>Научный журнал «Интегральная философия».</p>",
            articles=[{"type": "article", "value": {"title": "Интегральный метод в исследованиях", "authors": "Иванов А., Петрова Б.", "abstract": "Методологическая рамка для междисциплинарных работ.", "url": "https://allunity.ru/journal.shtml"}}],
            publication_date=datetime.date(2024, 6, 1),
        )
        root.add_child(instance=journal_page)
        Page.fix_tree()

        # Ensure library exists at root level
        library = root.get_children().filter(slug="library").first()
        if library:
            library.delete()
            Page.fix_tree()
        library_page = LibraryPage(
            slug="library",
            title="Библиотека",
            live=True, show_in_menus=True, first_published_at=timezone.now(),
            description="<p>Ресурсы по интегральной философии.</p>",
        )
        root.add_child(instance=library_page)
        Page.fix_tree()

        print("[sync_content] Site content synchronized")
    except Exception as e:
        print(f"[sync_content] Error: {e}", file=sys.stderr)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_seed_content"),
        ("content", "0001_initial"),
        ("home", "0001_initial"),
    ]

    # Django will drop these orphaned DB records when THIS migration applies
    replaces = [
        ("core", "0002_run_migrate_data"),
        ("core", "0002_sync_pages"),
        ("core", "0002_refresh_home"),
    ]

    operations = [
        migrations.RunPython(sync_content, migrations.RunPython.noop),
    ]