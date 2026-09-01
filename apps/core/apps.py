from django.apps import AppConfig
from django.db.models.signals import post_migrate
import sys


REAL_HOME_BODY = [
    ("heading", "Манифест неовсеединства"),
    ("paragraph", "На пути к обществу развития. Философия неовсеединства формулирует принципы эволюции и синтеза на основе принципов всеединства."),
    ("heading", "Интегральный кодекс"),
    ("paragraph", "Философская система синтеза, соединяющая принципы универсальности и строгости. Состоит из теоретической, этической и прикладной частей."),
    ("heading", "Разделы сообщества"),
    ("paragraph", "Журнал, форум, библиотека, исследования, проекты и образовательные программы."),
]


def ensure_content_pages(sender, **kwargs):
    print("[core.apps] signal fired", file=sys.stderr)
    try:
        from wagtail.models import Page
        from apps.content.models import JournalPage, LibraryPage
        from apps.home.models import HomePage
    except Exception as e:
        print(f"[core.apps] import failed: {e}", file=sys.stderr)
        return
    try:
        root = Page.objects.get(depth=1)
        home = root.get_children().filter(slug="home").first()
    except Exception as e:
        print(f"[core.apps] page lookup failed: {e}", file=sys.stderr)
        return
    if not home:
        print("[core.apps] home page not found", file=sys.stderr)
        return
    try:
        specific = home.specific
        if isinstance(specific, HomePage):
            specific.hero_title = "Интегральное сообщество"
            specific.hero_subtitle = "Консолидация всех конструктивных сил на основе принципов интегральной философии"
            specific.body = REAL_HOME_BODY
            specific.save(update_fields=["hero_title", "hero_subtitle", "body"])
            print("[core.apps] updated home", file=sys.stderr)
        else:
            print(f"[core.apps] home is not HomePage: {type(specific)}", file=sys.stderr)
    except Exception as e:
        print(f"[core.apps] failed to update home: {e}", file=sys.stderr)
    for model, slug in ((JournalPage, "journal"), (LibraryPage, "library")):
        try:
            if not root.get_children().filter(slug=slug).exists():
                page = model(slug=slug, title="Журнал «Интегральная философия»" if model.__name__ == "JournalPage" else "Библиотека", show_in_menus=True, live=True)
                root.add_child(instance=page)
                print(f"[core.apps] created {slug}", file=sys.stderr)
        except Exception as e:
            print(f"[core.apps] failed to create {slug}: {e}", file=sys.stderr)


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        post_migrate.connect(ensure_content_pages, sender=self)
