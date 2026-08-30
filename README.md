# AllUnity — Wagtail rebuild

Рефакторинг / редизайн / реверс-инжиниринг сайта **AllUnity.ru** на платформе
**Wagtail** (Django CMS). Генерирует полную структуру страниц, DRY-шаблоны
(общий `base.html` + `components/navigation.html` + `components/footer.html`),
кастомные StreamField-блоки, рабочий поиск, RSS-ленту и idempotent-скрипт
миграции контента со старого SHTML-сайта.

## Быстрый старт (SQLite, без внешних сервисов)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/development.txt beautifulsoup4
export DJANGO_SETTINGS_MODULE=allunity.settings.development
export SECRET_KEY=dev-insecure-key
python manage.py migrate
python manage.py createsuperuser
python manage.py migrate_data        # наполнить контентом с allunity.ru
python manage.py runserver
# сайт:    http://127.0.0.1:8000/
# админка: http://127.0.0.1:8000/admin/
```

## Структура

- `apps/core`        — `BasePage` (SEO/OG миксин), `blocks.py`, `management/commands/migrate_data.py`
- `apps/home`        — `HomePage`, `SearchPage`
- `apps/institute`   — `InstituteIndexPage`, `SubjectPage`, `LaboratoryPage`
- `apps/news`        — `NewsIndexPage`, `NewsPage`, `feeds.py` (RSS)
- `apps/projects`    — `ProjectIndexPage`, `ProjectPage`
- `apps/discussions` — `DiscussionIndexPage`, `DiscussionPage`
- `apps/content`     — `ManifestPage`, `CodexPage`, `DictionaryPage`, `SchoolPage`, `HistoryPage`, `EmblemPage`
- `templates/`       — `base.html`, `components/` (navigation, footer, breadcrumbs), page-шаблоны
- `allunity/settings` — `base / development / production`

## Возможности

- Полная структура: Главная, Манифест, Кодекс (8 статей), Институт (+5 предметов),
  Новости (RSS), Проекты, Словарь, Школа, История, Эмблема, Дискуссии, Поиск.
- Рабочий поиск (`SearchPage`, Wagtail search backend) + поле поиска в шапке.
- RSS-лента новостей: `/news/rss/`.
- Хлебные крошки, адаптивная навигация (Alpine.js), доступность (skip-link, aria-label, focusable main).
- `sitemap.xml` (Wagtail sitemaps).
- Favicon-сет (`static/favicon/`).

## Миграция контента со старого сайта

```bash
python manage.py migrate_data --dry-run   # проверка без записи
python manage.py migrate_data             # парсинг allunity.ru и создание страниц
```

Скрипт (`apps/core/management/commands/migrate_data.py`) идемпотентен: очищает
дочерние страницы, исправляет treebeard-метаданные (`Page.fix_tree`) и пересоздаёт
дерево. Контент реальных разделов (Кодекс, Словарь, Школа, История) парсится с
live-сайта или заполняется осмысленными примерами.

## Производство / деплой

- `docker-compose up --build` поднимает web + db (Postgres) + redis + nginx.
- Настройки prod читают `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL` (через
  `dj-database-url`), `REDIS_URL` из окружения. Скопируйте `.env.example` → `.env`.
- Security: `SECURE_HSTS_PRELOAD`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
  SSL-редирект (nginx терминирует TLS). Проверка: `check --deploy`.

## Тестирование и CI

```bash
python manage.py check
python manage.py test apps
```

GitHub Actions (`ci.yml`) запускает `check` + проверку миграций + тесты + шаг
воспроизводимости миграции (`migrate` + `migrate_data` + assert счётчиков страниц).

## Заметки

- Навигация строится из `site_root.get_children.live.in_menu` — все основные
  разделы помечены `show_in_menus=True` при миграции.
- `wagtail.contrib.modeladmin` помечен deprecated в Wagtail 6 (работает в 5.2).
