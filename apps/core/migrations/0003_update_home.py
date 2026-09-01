from django.db import migrations


def update_home(apps, schema_editor):
    from wagtail.models import Page
    from apps.home.models import HomePage
    try:
        root = Page.objects.get(depth=1)
        home = root.get_children().filter(slug="home").first()
        if not home:
            return
        home = home.specific
        if isinstance(home, HomePage):
            home.hero_title = "Интегральное сообщество"
            home.hero_subtitle = "Консолидация всех конструктивных сил на основе принципов интегральной философии"
            home.body = [
                ("heading", "Манифест неовсеединства"),
                ("paragraph", "На пути к обществу развития. Философия неовсеединства формулирует принципы эволюции и синтеза на основе принципов всеединства."),
                ("heading", "Интегральный кодекс"),
                ("paragraph", "Философская система синтеза, соединяющая принципы универсальности и строгости. Состоит из теоретической, этической и прикладной частей."),
                ("heading", "Разделы сообщества"),
                ("paragraph", "Журнал, форум, библиотека, исследования, проекты и образовательные программы."),
            ]
            home.save(update_fields=["hero_title", "hero_subtitle", "body"])
    except Exception as e:
        print(f"[0003_update_home] failed: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_noop"),
    ]

    operations = [migrations.RunPython(update_home, migrations.RunPython.noop)]
