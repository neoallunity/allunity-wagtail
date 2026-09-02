import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "allunity.settings.prod")


def fix_migrations():
    """Remove orphaned migration records BEFORE Django loads them.

    Django refuses to start if django_migrations contains records with no
    matching migration file (ConflictingMigrationHistory).  We delete the
    stale rows via raw pymysql so Django can boot cleanly.
    """
    try:
        import pymysql
        from urllib.parse import urlparse

        url = os.environ.get("DATABASE_URL", "")
        if "mysql" not in url:
            return

        parsed = urlparse(url)
        conn = pymysql.connect(
            host=parsed.hostname,
            port=parsed.port or 3306,
            user=parsed.username,
            password=parsed.password or "",
            database=parsed.path.lstrip("/"),
            connect_timeout=5,
        )
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM django_migrations "
                "WHERE app = 'core' AND name LIKE '0002_%'"
            )
            conn.commit()
            deleted = cur.rowcount or 0
            print(
                f"[wsgi] Cleaned orphaned core.0002_* migration records "
                f"({deleted} rows)",
                file=sys.stderr,
            )
        conn.close()
    except Exception as e:
        print(
            f"[wsgi] Migration cleanup skipped: "
            f"{type(e).__name__}: {e}",
            file=sys.stderr,
        )


fix_migrations()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


def sync_content():
    """Synchronize content from real allunity.ru data on each boot."""
    try:
        from django.utils import timezone
        from wagtail.models import Page, Site
        from apps.home.models import HomePage
        from apps.content.models import JournalPage, LibraryPage

        root = Page.objects.get(depth=1)

        # Update home page
        home = root.get_children().filter(slug="home").first()
        if home:
            hp = HomePage.objects.get(id=home.id)
            if hp.hero_title != "Интегральное сообщество":
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
                print("[wsgi] HomePage updated!", file=sys.stderr)
        else:
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

            print("[wsgi] HomePage created!", file=sys.stderr)

        # Ensure journal/library exist
        for model_cls, slug, title in [
            (JournalPage, "journal",
             "Журнал «Интегральная философия»"),
            (LibraryPage, "library", "Библиотека"),
        ]:
            if not root.get_children().filter(slug=slug).exists():
                page = model_cls(
                    slug=slug, title=title,
                    show_in_menus=True, live=True,
                    first_published_at=timezone.now(),
                )
                root.add_child(instance=page)
                Page.fix_tree()

        print("[wsgi] Content synchronized!", file=sys.stderr)
    except Exception as e:
        print(
            f"[wsgi] sync skipped: {type(e).__name__}: {e}",
            file=sys.stderr,
        )


if "runserver" not in sys.argv and "test" not in sys.argv:
    print("[wsgi] Starting content sync...", file=sys.stderr)
    sync_content()
    print("[wsgi] Content sync complete.", file=sys.stderr)
