from django.db import migrations


SQL_CLEANUP_ORPHANED = """
DELETE FROM wagtailcore_page WHERE path LIKE '0001%' AND depth > 1;
DELETE FROM wagtailcore_site WHERE root_page_id IS NULL OR root_page_id NOT IN (SELECT id FROM wagtailcore_page);
"""


SQL_UPDATE_HOME = """
UPDATE home_homepage SET 
    hero_title = 'Интегральное сообщество',
    hero_subtitle = 'Консолидация всех конструктивных сил на основе принципов интегральной философии'
WHERE page_ptr_id IN (SELECT p.id FROM wagtailcore_page p WHERE p.slug = 'home' AND p.depth > 1);
"""


class Migration(migrations.Migration):

    replaces = [
        ("core", "0002_run_migrate_data"),
        ("core", "0002_sync_pages"),
        ("core", "0002_refresh_home"),
        ("core", "0002_sync_fix"),
    ]

    dependencies = [
        ("core", "0001_seed_content"),
        ("content", "0001_initial"),
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(SQL_CLEANUP_ORPHANED),
        migrations.RunSQL(SQL_UPDATE_HOME),
    ]