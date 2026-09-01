from django.apps import AppConfig
from django.db.models.signals import post_migrate


def ensure_content_pages(sender, **kwargs):
    import sys
    if "test" in sys.argv:
        return
    
    from django.utils import timezone
    from wagtail.models import Page, Site
    from apps.home.models import HomePage
    
    try:
        root = Page.objects.get(depth=1)
        home = root.get_children().filter(slug="home").first()
        
        if home:
            # Delete and recreate with new content
            home.delete()
            Page.fix_tree()
        
        home = HomePage(
            slug="home",
            title="Интегральное сообщество",
            hero_title="Интегральное сообщество",
            hero_subtitle="Консолидация всех конструктивных сил на основе принципов интегральной философии",
            show_in_menus=True,
            live=True,
            first_published_at=timezone.now(),
        )
        root.add_child(instance=home)
        Page.fix_tree()
        
        site = Site.objects.first()
        site.root_page = home
        site.save()
        
        print("[apps.core] HomePage updated")
    except Exception as e:
        print(f"[apps.core] Failed: {e}", file=sys.stderr)


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        post_migrate.connect(ensure_content_pages, sender=self)