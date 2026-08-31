from django.db import migrations


REAL_HOME_BODY = [
    ("heading", "Манифест неовсеединства"),
    ("paragraph", "На пути к обществу развития. Философия неовсеединства формулирует принципы эволюции и синтеза на основе принципов всеединства."),
    ("heading", "Интегральный кодекс"),
    ("paragraph", "Философская система синтеза, соединяющая принципы универсальности и строгости. Состоит из теоретической, этической и прикладной частей."),
    ("heading", "Разделы сообщества"),
    ("paragraph", "Журнал, форум, библиотека, исследования, проекты и образовательные программы."),
]


def update_home_content(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    HomePage = apps.get_model("home", "HomePage")
    try:
        home = Page.objects.filter(slug="home").first()
        if not home:
            return
        specific = home.specific
        specific.hero_title = "Интегральное сообщество"
        specific.hero_subtitle = "Консолидация всех конструктивных сил на основе принципов интегральной философии"
        specific.body = REAL_HOME_BODY
        specific.save()
    except Exception as e:
        print(f"[update_home_content] failed: {type(e).__name__}: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0003_searchpage"),
        ("core", "0001_seed_content"),
    ]

    operations = [migrations.RunPython(update_home_content, migrations.RunPython.noop)]
