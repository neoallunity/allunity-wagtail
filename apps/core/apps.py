from django.apps import AppConfig
from django.db.models.signals import post_migrate


def ensure_content_pages(sender, **kwargs):
    if kwargs.get("plan") and not kwargs.get("run_migrations"):
        return
    from wagtail.models import Page
    try:
        from apps.content.models import JournalPage, LibraryPage
    except Exception:
        return
    root = Page.objects.get(depth=1)
    home = root.get_children().filter(slug="home").first()
    if not home:
        return
    for model, slug in ((JournalPage, "journal"), (LibraryPage, "library")):
        if not home.get_children().filter(slug=slug).exists():
            page = model(slug=slug, show_in_menus=True, live=True)
            home.add_child(instance=page)


class CoreConfig(AppConfig):
    name = "apps.core"
    def ready(self):
        post_migrate.connect(ensure_content_pages, sender=self)
