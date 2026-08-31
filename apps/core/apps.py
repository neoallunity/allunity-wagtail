from django.apps import AppConfig
from django.db.models.signals import post_migrate


def ensure_content_pages(sender, **kwargs):
    if kwargs.get("plan") and not kwargs.get("run_migrations"):
        return
    try:
        from wagtail.models import Page
        from apps.content.models import JournalPage, LibraryPage
    except Exception:
        return
    try:
        root = Page.objects.get(depth=1)
        home = root.get_children().filter(slug="home").first()
    except Exception:
        return
    if not home:
        return
    for model, slug in ((JournalPage, "journal"), (LibraryPage, "library")):
        if not home.get_children().filter(slug=slug).exists():
            try:
                page = model(slug=slug, title="Журнал «Интегральная философия»" if model.__name__ == "JournalPage" else "Библиотека", show_in_menus=True, live=True)
                home.add_child(instance=page)
            except Exception as e:
                print(f"[core.apps] failed to create {slug}: {e}")


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        post_migrate.connect(ensure_content_pages, sender=self)
