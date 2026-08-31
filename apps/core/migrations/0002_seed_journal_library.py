"""Ensure JournalPage and LibraryPage exist on production after deploy."""
from django.db import migrations
import datetime


REAL_JOURNAL = {
    "title": "Журнал «Интегральная философия»",
    "volume": "№ 15",
    "publication_date": datetime.date(2024, 6, 1),
    "description": "<p>Научный журнал «Интегральная философия» предоставляет площадку для выражения своих позиций участникам Интегрального сообщества.</p>",
    "articles": [
        {"type": "article", "value": {
            "title": "Интегральный метод в исследованиях",
            "authors": "Иванов А., Петрова Б.",
            "abstract": "Методологическая рамка для междисциплинарных работ.",
            "url": "https://allunity.ru/journal.shtml",
        }},
        {"type": "article", "value": {
            "title": "Этика развития",
            "authors": "Сидоров В.",
            "abstract": "Нравственные основания принципов неовсеединства.",
            "url": "https://allunity.ru/journal.shtml",
        }},
    ],
}
REAL_LIBRARY = {
    "title": "Библиотека",
    "description": "<p>Ресурсы по интегральной философии и смежным областям.</p>",
    "resources": [
        {"type": "resource", "value": {
            "title": "Всеединство: anthology",
            "author": "AllUnity",
            "resource_type": "Подборка",
            "url": "https://allunity.ru/library.shtml",
            "description": "Собрание ключевых текстов по теме всеединства.",
        }},
        {"type": "resource", "value": {
            "title": "Журнал «Интегральная философия»",
            "author": "AllUnity",
            "resource_type": "Журнал",
            "url": "https://allunity.ru/journal.shtml",
            "description": "Периодическое издание сообщества.",
        }},
    ],
}


def seed_journal_library(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    JournalPage = apps.get_model("content", "JournalPage")
    LibraryPage = apps.get_model("content", "LibraryPage")

    try:
        root = Page.objects.get(depth=1)
        home = root.get_children().filter(slug="home").first()
    except Exception as e:
        print(f"[seed_journal_library] tree lookup failed: {e}")
        return
    if not home:
        print("[seed_journal_library] home not found")
        return

    def upsert(parent, model, slug, **fields):
        try:
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
        except Exception as e:
            print(f"[seed_journal_library] upsert {slug} failed: {type(e).__name__}: {e}")

    upsert(home, JournalPage, "journal", **REAL_JOURNAL)
    upsert(home, LibraryPage, "library", **REAL_LIBRARY)


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0005_librarypage_journalpage"),
        ("core", "0001_seed_content"),
    ]

    operations = [migrations.RunPython(seed_journal_library, migrations.RunPython.noop)]
