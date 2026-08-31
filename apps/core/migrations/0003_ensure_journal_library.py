from django.db import migrations
import datetime


def ensure_journal_library(apps, schema_editor):
    from wagtail.models import Page
    JournalPage = apps.get_model("content", "JournalPage")
    LibraryPage = apps.get_model("content", "LibraryPage")

    root = Page.objects.get(depth=1)
    home = root.get_children().filter(slug="home").first()
    if not home:
        return

    def upsert(parent, model, slug, **fields):
        existing = parent.get_children().filter(slug=slug).first()
        if existing:
            for k, v in fields.items():
                setattr(existing.specific, k, v)
            existing.specific.show_in_menus = True
            existing.specific.save()
            return existing.specific
        page = model(slug=slug, show_in_menus=True, **fields)
        parent.add_child(instance=page)
        return page

    upsert(home, JournalPage, "journal",
           title="Журнал «Интегральная философия»",
           volume="№ 15",
           publication_date=datetime.date(2024, 6, 1),
           description="<p>Научный журнал «Интегральная философия».</p>",
           articles=[
               {"type": "article", "value": {
                   "title": "Интегральный метод в исследованиях",
                   "authors": "Иванов А., Петрова Б.",
                   "abstract": "Методологическая рамка для междисциплинарных работ.",
                   "url": "https://allunity.ru/journal.shtml",
               }},
           ])
    upsert(home, LibraryPage, "library",
           title="Библиотека",
           description="<p>Ресурсы по интегральной философии и смежным областям.</p>",
           resources=[
               {"type": "resource", "value": {
                   "title": "Всеединство: anthology",
                   "author": "AllUnity",
                   "resource_type": "Подборка",
                   "url": "https://allunity.ru/library.shtml",
                   "description": "Собрание ключевых текстов по теме всеединства.",
               }},
           ])


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0005_librarypage_journalpage"),
        ("core", "0002_update_home_content"),
    ]

    operations = [migrations.RunPython(ensure_journal_library)]
