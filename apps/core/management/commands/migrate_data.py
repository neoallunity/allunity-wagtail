from django.core.management.base import BaseCommand
from wagtail.models import Site, Page
from apps.home.models import HomePage, SearchPage
from apps.institute.models import InstituteIndexPage, SubjectPage
from apps.news.models import NewsIndexPage, NewsPage
from apps.projects.models import ProjectIndexPage, ProjectPage
from apps.content.models import ManifestPage, CodexPage, DictionaryPage, SchoolPage, HistoryPage, EmblemPage
from apps.discussions.models import DiscussionIndexPage, DiscussionPage
from bs4 import BeautifulSoup
from wagtail.rich_text import RichText


class Command(BaseCommand):
    help = "Migrate content from old AllUnity SHTML site into Wagtail (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Run without writing.")

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        self.root = Page.objects.get(depth=1)
        self.clear_children()
        self.create_home()
        self.create_institute()
        self.create_news()
        self.create_projects()
        self.seed_news()
        self.seed_projects()
        self.create_manifest()
        self.create_discussions()
        self.create_content_pages()
        self.create_search()
        self.stdout.write(self.style.SUCCESS("Migration completed."))

    def clear_children(self):
        """Remove any previously-created pages under root so the run is repeatable."""
        if self.dry_run:
            return
        for child in self.root.get_children():
            child.delete()
        # treebeard can leave numchild/path metadata stale after deletes
        Page.fix_tree()
        self.root.refresh_from_db()

    def upsert(self, parent, model, slug, **fields):
        """Create a page under `parent`; if slug exists under parent, reuse it."""
        if self.dry_run:
            return None
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

    def create_home(self):
        self.stdout.write("Creating HomePage...")
        home = self.upsert(
            self.root, HomePage, "home",
            title="AllUnity — Интегральная философия и наука",
            hero_title="Добро пожаловать в AllUnity",
            hero_subtitle="Философия, наука и искусство в едином целом",
            body=self.parse_streamfield(self.fetch("https://allunity.ru/index.shtml")),
        )
        self.home_page = home
        if home and not self.dry_run:
            site, _ = Site.objects.get_or_create(
                is_default_site=True,
                defaults={"hostname": "localhost", "port": 80, "root_page": home, "site_name": "AllUnity"},
            )
            site.root_page = home
            site.save()

    def create_institute(self):
        self.stdout.write("Creating Institute...")
        inst = self.upsert(
            self.home_page, InstituteIndexPage, "institute",
            title="Институт",
            introduction="<p>Образовательные программы AllUnity</p>",
        )
        if not inst or self.dry_run:
            return
        for slug, title, desc in [
            ("etics", "Этика", "Моральные принципы и этические системы"),
            ("word", "Словесность", "Литература, риторика, языкознание"),
            ("math", "Математика", "Математические основы философии"),
            ("hist", "История", "История идей"),
            ("law", "Право", "Правовые основы общества"),
        ]:
            self.upsert(
                inst, SubjectPage, slug,
                title=title, search_description=desc, difficulty_level="intermediate",
                subject_code=slug.upper(),
                introduction=f"<p>{desc}</p>",
                curriculum=self.parse_curriculum(self.fetch(f"https://allunity.ru/{slug}.shtml")),
            )

    def create_news(self):
        self.stdout.write("Creating News...")
        self.upsert(self.home_page, NewsIndexPage, "news", title="Новости")

    def create_projects(self):
        self.stdout.write("Creating Projects...")
        self.upsert(self.home_page, ProjectIndexPage, "projects",
                    title="Проекты", introduction="<p>Исследовательские проекты AllUnity</p>")

    def seed_news(self):
        self.stdout.write("Seeding News entries...")
        news_index = NewsIndexPage.objects.live().first()
        if not news_index or self.dry_run:
            return
        titles = [
            "Создан Институт интегральной науки",
            "Готовится 15-й выпуск журнала",
            "Обновление сайта сообщества",
            "Развитие проекта «Математизация философии»",
        ]
        for i, title in enumerate(titles):
            slug = "news-" + str(i + 1)
            self.upsert(
                news_index, NewsPage, slug,
                title=title, author="AllUnity",
                body=[("paragraph", f"<p>{title}. Подробности — в официальных каналах сообщества.</p>")],
            )

    def seed_projects(self):
        self.stdout.write("Seeding Project entries...")
        proj_index = ProjectIndexPage.objects.live().first()
        if not proj_index or self.dry_run:
            return
        projects = [
            ("Неовсеединство", "active", "Синтез метафизики всеединства и современной науки."),
            ("Интегралика", "active", "Интегральный подход к образованию и развитию личности."),
            ("Единое знание", "planning", "Единая система знания across дисциплин."),
            ("Интегральная медицина", "planning", "Целостный подход к здоровью и практике."),
            ("Математизация философии", "active", "Формализация философских категорий средствами математики."),
        ]
        for i, (name, status, desc) in enumerate(projects):
            slug = "project-" + str(i + 1)
            self.upsert(
                proj_index, ProjectPage, slug,
                title=name, project_status=status,
                overview=RichText(f"<p>{desc}</p>"),
            )

    def create_manifest(self):
        self.stdout.write("Creating Manifest...")
        self.upsert(
            self.home_page, ManifestPage, "manifest",
            title="Манифест AllUnity",
            introduction="<p>Интегральное видение будущего человечества и планеты.</p>",
            body=self.parse_streamfield(self.fetch("https://allunity.ru/manifest.shtml")),
        )

    def create_search(self):
        self.stdout.write("Creating Search page...")
        self.upsert(self.home_page, SearchPage, "search", title="Поиск",
                    intro="<p>Поиск по материалам AllUnity.</p>")

    def create_discussions(self):
        self.stdout.write("Creating Discussions...")
        self.upsert(self.home_page, DiscussionIndexPage, "discussions", title="Дискуссии")

    def create_content_pages(self):
        self.stdout.write("Creating content pages...")
        ph = "<p>Раздел наполняется.</p>"
        self.upsert(self.home_page, CodexPage, "codex",
                    title="Кодекс", preamble="<p>Этический и поведенческий кодекс сообщества.</p>",
                    articles=self.parse_articles(self.fetch("https://allunity.ru/codex.shtml")))
        self.upsert(self.home_page, DictionaryPage, "dictionary", title="Словарь",
                    terms=self.parse_terms())
        self.upsert(self.home_page, SchoolPage, "school",
                    title="Школа", admission_requirements=ph, curriculum_overview=ph,
                    programs=self.parse_programs())
        self.upsert(self.home_page, HistoryPage, "history", title="История",
                    timeline=self.parse_timeline())
        self.upsert(self.home_page, EmblemPage, "emblem",
                    title="Эмблема", symbolism=ph, history_of_creation=ph, usage_guidelines=ph)

    def parse_terms(self):
        terms = [
            ("Интегральная философия", "Направление мысли, стремящееся к синтезу всех уровней познания — научного, философского, художественного и духовного."),
            ("Неовсеединство", "Современное развитие идеи всеединства: признание многообразия при сохранении фундаментального единства бытия."),
            ("Синтез", "Метод соединения противоположностей в более широкое, непротиворечивое целое."),
        ]
        blocks = []
        for word, definition in terms:
            blocks.append({"type": "term", "value": {
                "word": word, "definition": "<p>" + definition + "</p>",
                "etymology": "от греч. / лат. корней соответствующих понятий",
                "related_terms": [t[0] for t in terms if t[0] != word][:2]}})
        return blocks

    def parse_programs(self):
        programs = [
            ("Основы интегральной философии", "1 год", "Введение в принципы всеединства и методы синтеза."),
            ("Интегральная практика", "2 года", "Прикладные методы развития личности и преобразования мышления."),
        ]
        blocks = []
        for name, duration, desc in programs:
            blocks.append({"type": "program", "value": {
                "name": name, "duration": duration, "description": "<p>" + desc + "</p>",
                "subjects": ["Этика", "Математика", "Словесность"]}})
        return blocks

    def parse_timeline(self):
        events = [
            ("2015", "Основание Интегрального сообщества", "Начало систематической работы по консолидации направлений."),
            ("2018", "Создание Института интегральной науки (ИИН)", "Объединение исследовательских программ сообщества."),
            ("2021", "Запуск периодического издания", "Выпуск журнала интегральной философии и науки."),
            ("2026", "Обновление цифровой платформы", "Переход на современный CMS-движок сайта."),
        ]
        blocks = []
        for date, title, desc in events:
            blocks.append({"type": "event", "value": {
                "date": date + "-01-01", "title": title, "description": "<p>" + desc + "</p>"}})
        return blocks

    def parse_articles(self, html):
        """Group content under each 'Статья N' heading into RichText article blocks.
        Use plain strings (not RichText) — the articles field is a JSON column and
        Wagtail serializes StreamValue to JSON; RichText objects are not JSON-serializable."""
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        blocks = []
        current = None
        buf = []
        for el in soup.find_all(["h2", "h3", "h4", "p"]):
            txt = el.get_text(strip=True)
            if el.name in ("h2", "h3", "h4") and "статья" in txt.lower():
                if current is not None:
                    blocks.append({"type": "article", "value": {
                        "title": current, "content": "<p>" + " ".join(buf) + "</p>"}})
                current = txt
                buf = []
            elif current is not None and el.name == "p" and txt:
                buf.append(txt)
        if current is not None:
            blocks.append({"type": "article", "value": {
                "title": current, "content": "<p>" + " ".join(buf) + "</p>"}})
        return blocks

    def fetch(self, url):
        try:
            import urllib.request
            return urllib.request.urlopen(url, timeout=10).read().decode("utf-8", "replace")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"fetch {url}: {e}"))
            return ""

    def parse_streamfield(self, html):
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        blocks = []
        for el in soup.find_all(["h1", "h2", "h3", "p"]):
            txt = el.get_text(strip=True)
            if not txt:
                continue
            if el.name in ("h1", "h2", "h3"):
                blocks.append(("heading", txt))
            else:
                blocks.append(("paragraph", txt))
        return blocks

    def parse_curriculum(self, html):
        return [{
            "type": "module",
            "value": {
                "title": "Введение",
                "description": "<p>Основные концепции и принципы</p>",
                "lessons": [
                    {"type": "lesson_title", "value": "Урок 1: Основы"},
                    {"type": "lesson_content", "value": "<p>Введение в предмет</p>"},
                ],
            },
        }]
