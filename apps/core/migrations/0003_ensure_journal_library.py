from django.db import migrations


def ensure_journal_library(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    JournalPage = apps.get_model("content", "JournalPage")
    LibraryPage = apps.get_model("content", "LibraryPage")

    try:
        root = Page.objects.get(depth=1)
        home = root.get_children().filter(slug="home").first()
    except Exception:
        return

    if not home:
        return

    for model, slug in ((JournalPage, "journal"), (LibraryPage, "library")):
        try:
            if not root.get_children().filter(slug=slug).exists():
                page = model(
                    slug=slug,
                    title="Журнал «Интегральная философия»" if model.__name__ == "JournalPage" else "Библиотека",
                    show_in_menus=True,
                    live=True,
                )
                root.add_child(instance=page)
        except Exception as e:
            print(f"[0003_ensure_journal_library] failed to create {slug}: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0005_librarypage_journalpage"),
        ("core", "0002_update_home_content"),
    ]

    operations = [migrations.RunPython(ensure_journal_library)]
