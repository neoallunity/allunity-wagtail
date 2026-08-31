from django.apps import AppConfig
from django.db.models.signals import post_migrate


REAL_HOME_BODY = [
    ("heading", "Манифест неовсеединства"),
    ("paragraph", "На пути к обществу развития. Философия неовсеединства формулирует принципы эволюции и синтеза на основе принципов всеединства."),
    ("heading", "Интегральный кодекс"),
    ("paragraph", "Философская система синтеза, соединяющая принципы универсальности и строгости. Состоит из теоретической, этической и прикладной частей."),
    ("heading", "Разделы сообщества"),
    ("paragraph", "Журнал, форум, библиотека, исследования, проекты и образовательные программы."),
]


def ensure_content_pages(sender, **kwargs):
    if kwargs.get("plan") and not kwargs.get("run_migrations"):
        return
    try:
        from wagtail.models import Page
        from apps.content.models import JournalPage, LibraryPage
        from apps.home.models import HomePage
    except Exception:
        return
    try:
        root = Page.objects.get(depth=1)
        home = root.get_children().filter(slug="home").first()
        if not home:
            return
        home = home.specific
    except Exception:
        return
    if not isinstance(home, HomePage):
        return
    try:
        home.hero_title = "Интегральное сообщество"
        home.hero_subtitle = "Консолидация всех конструктивных сил на основе принципов интегральной философии"
        home.body = REAL_HOME_BODY
        home.save(update_fields=["hero_title", "hero_subtitle", "body"])
    except Exception as e:
        print(f"[core.apps] failed to update home: {e}")
    for model, slug in ((JournalPage, "journal"), (LibraryPage, "library")):
        if not home.get_parent().get_children().filter(slug=slug).exists():
            try:
                page = model(slug=slug, title="Журнал «Интегральная философия»" if model.__name__ == "JournalPage" else "Библиотека", show_in_menus=True, live=True)
                home.get_parent().add_child(instance=page)
            except Exception as e:
                print(f"[core.apps] failed to create {slug}: {e}")


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        post_migrate.connect(ensure_content_pages, sender=self)
