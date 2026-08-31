from django.db import migrations
import datetime


REAL_HOME_BODY = [
    ("heading", "Манифест неовсеединства"),
    ("paragraph", "На пути к обществу развития. Философия неовсеединства формулирует принципы эволюции общества на основе интегрального подхода, соединяющего науку, культуру и духовные ценности."),
    ("heading", "Интегральный подход"),
    ("paragraph", "Проект AllUnity объединяет исследования, образование и общественные инициативы для создания устойчивого будущего через диалог и синтез разных традиций мышления."),
    ("heading", "Присоединяйтесь"),
    ("paragraph", "Изучайте материалы, участвуйте в дискуссиях и развивайте интегральное мировоззрение вместе с сообществом."),
]


def refresh_home(apps, schema_editor):
    HomePage = apps.get_model("home", "HomePage")
    page = HomePage.objects.filter(slug="home").first()
    if not page:
        return
    body = []
    for kind, text in REAL_HOME_BODY:
        if kind == "heading":
            body.append(("heading", text))
        else:
            body.append(("paragraph", text))
    page.body = body
    page.save(update_fields=["body"])


class Migration(migrations.Migration):
    dependencies = [("core", "0001_seed_content")]

    operations = [migrations.RunPython(refresh_home, migrations.RunPython.noop)]
