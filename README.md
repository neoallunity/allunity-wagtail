# AllUnity — Wagtail rebuild

Рефакторинг / редизайн / реверсинжиниринг сайта **AllUnity.ru** на платформе
**Wagtail** (Django CMS). Генерирует полную структуру страниц, DRY-шаблоны
(общий `base.html` + `components/navigation.html` + `components/footer.html`),
кастомные StreamField-блоки и скрипт миграции контента со старого SHTML-сайта.

## Быстрый старт (SQLite, без внешних сервисов)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/development.txt
export DJANGO_SETTINGS_MODULE=allunity.settings.development
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# admin: http://127.0.0.1:8000/admin/
```

## Структура

- `apps/core`      — `BasePage` (SEO/OG миксин), `blocks.py`, `middleware.py`
- `apps/home`      — `HomePage` (hero + StreamField body)
- `apps/institute` — `InstituteIndexPage`, `SubjectPage`, `LaboratoryPage`
- `apps/news`      — `NewsIndexPage`, `NewsPage`
- `apps/projects`  — `ProjectIndexPage`, `ProjectPage`
- `apps/discussions` — `DiscussionIndexPage`, `DiscussionPage`
- `apps/content`   — `ManifestPage`, `CodexPage`, `DictionaryPage`, `SchoolPage`, `HistoryPage`, `EmblemPage`
- `templates/`     — `base.html`, `components/`, `blocks/`, page-шаблоны
- `allunity/settings` — `base / development / production / testing`

## Миграция контента со старого сайта

```bash
python manage.py migrate_data --dry-run   # проверка без записи
python manage.py migrate_data             # парсинг allunity.ru и создание страниц
```

Скрипт (`apps/core/management/commands/migrate_data.py`) обходит SHTML-страницы,
превращает `<h1>/<h2>/<p>` в StreamField-блоки и создаёт дерево Wagtail-страниц.

## Производство

- Postgres: задайте `DATABASE_URL=postgres://...`
- Redis-кэш: `REDIS_URL=redis://...` (опционально)
- `docker-compose up --build` поднимает web + db + redis + nginx (SSL в ./ssl)

## Заметки

- `apps.core.middleware.SecurityHeadersMiddleware` добавляет заголовки безопасности.
- `templates/components/navigation.html` строит меню из `site_root.get_children.live.in_menu`
  (включите «Show in menus» у нужных страниц в админке).
