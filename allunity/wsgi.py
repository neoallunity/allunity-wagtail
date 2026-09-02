import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "allunity.settings.prod")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


def sync_content():
    """Synchronize content from real allunity.ru data on first boot."""
    try:
        from django.utils import timezone
        from wagtail.models import Page, Site

        root = Page.objects.get(depth=1)

        # Create/update home page
        existing = root.get_children().filter(slug="home").first()
        if existing:
            # Just update the fields, don't delete
            from apps.home.models import HomePage
            hp = HomePage.objects.get(id=existing.id)
            hp.hero_title = "Интегральное сообщество"
            hp.hero_subtitle = (
                "Консолидация всех конструктивных сил на основе "
                "принципов интегральной философии"
            )
            if not hp.body:
                hp.body = [
                    ("heading", "Манифест неовсеединства"),
                    ("paragraph",
                     "На пути к обществу развития. Философия "
                     "неовсеединства формулирует принципы."),
                ]
            hp.save()
            Page.fix_tree()
            print("[wsgi] HomePage updated", file=sys.stderr)
        else:
            from apps.home.models import HomePage
            from apps.content.models import JournalPage, LibraryPage

            home = HomePage(
                slug="home",
                title="Интегральное сообщество",
                hero_title="Интегральное сообщество",
                hero_subtitle=(
                    "Консолидация всех конструктивных сил на основе "
                    "принципов интегральной философии"
                ),
                show_in_menus=True,
                live=True,
                first_published_at=timezone.now(),
            )
            root.add_child(instance=home)
            Page.fix_tree()

            site = Site.objects.first()
            if site:
                site.root_page = home
                site.save()

            print("[wsgi] HomePage created", file=sys.stderr)

        # Ensure journal/library exist at root level
        from apps.content.models import JournalPage, LibraryPage
        for slug, title in [("journal",
                             "Журнал «Интегральная философия»"),
                            ("library", "Библиотека")]:
            if not root.get_children().filter(slug=slug).exists():
                page = JournalPage(
                    slug=slug, title=title,
                    show_in_menus=True, live=True,
                    first_published_at=timezone.now(),
                ) if slug == "journal" else LibraryPage(
                    slug=slug, title=title,
                    show_in_menus=True, live=True,
                    first_published_at=timezone.now(),
                )
                root.add_child(instance=page)
                Page.fix_tree()

        print("[wsgi] Content synchronized!", file=sys.stderr)
    except Exception as e:
        print(f"[wsgi] sync skipped: {type(e).__name__}: {e}",
              file=sys.stderr)


# Run content sync on every startup in production
if "runserver" not in sys.argv and "test" not in sys.argv:
    print("[wsgi] Starting content sync...", file=sys.stderr)
    sync_content()
    print("[wsgi] Content sync complete.", file=sys.stderr)
