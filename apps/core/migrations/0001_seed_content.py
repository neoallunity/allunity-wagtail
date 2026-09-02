from django.db import migrations


def create_ensure_content(apps, schema_editor):
    """Create site and update HomePage."""
    from django.utils import timezone
    from wagtail.models import Page, Site
    
    # Get root page
    root = Page.objects.get(depth=1)
    
    # Create/update HomePage
    home = HomePage = apps.get_model("home", "HomePage")
    
    existing = home.objects.filter(slug="home").first()
    if existing:
        existing.delete()
        Page.fix_tree()
    
    new_home = HomePage(
        slug="home",
        title="Интегральное сообщество",
        hero_title="Интегральное сообщество",
        hero_subtitle="Консолидация всех конструктивных сил на основе принципов интегральной философии",
        show_in_menus=True,
        live=True,
        first_published_at=timezone.now(),
    )
    root.add_child(instance=new_home)
    Page.fix_tree()
    
    # Set site
    site = Site.objects.first()
    site.root_page = new_home
    site.save()
    
    print("[0001] Site content created")


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(create_ensure_content, migrations.RunPython.noop),
    ]