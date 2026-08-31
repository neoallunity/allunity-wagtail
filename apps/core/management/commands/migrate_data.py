from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Site, Page
from apps.home.models import HomePage, SearchPage
from apps.institute.models import InstituteIndexPage, SubjectPage
from apps.news.models import NewsIndexPage, NewsPage
from apps.projects.models import ProjectIndexPage, ProjectPage
from apps.content.models import ManifestPage, CodexPage, DictionaryPage, SchoolPage, HistoryPage, EmblemPage, JournalPage, LibraryPage
from apps.discussions.models import DiscussionIndexPage, DiscussionPage
from bs4 import BeautifulSoup
from wagtail.rich_text import RichText
import datetime


REAL_CONTENT = {
    "home": {
        "hero_title": "Интегральное сообщество",
        "hero_subtitle": "Консолидация всех конструктивных сил на основе принципов интегральной философии",
        "body": [
            ("heading", "Манифест неовсеединства"),
            ("paragraph", "На пути к обществу развития. Философия неовсеединства формулирует принципы эволюции и синтеза на основе принципов всеединства."),
            ("heading", "Интегральный кодекс"),
            ("paragraph", "Философская система синтеза, соединяющая принципы универсальности и строгости. Состоит из теоретической, этической и прикладной частей."),
            ("heading", "Разделы сообщества"),
            ("paragraph", "Журнал, форум, библиотека, исследования, проекты и образовательные программы."),
        ],
    },
    "manifest": {
        "title": "Манифест философии неовсеединства",
        "introduction": "<p>На пути к обществу развития: всё бытие пронизывает процесс развития. Развивается ребёнок, развиваются виды в биологической эволюции, развиваются технологии, развивается Вселенная. Пришло время создания теории развития.</p>",
        "body": [
            ("heading", "Развитие как универсальный принцип"),
            ("paragraph", "Развитие — это не только внешнее изменение, но и внутреннее усложнение, условное обогащение и движение к более целостным формам."),
            ("heading", "Неовсеединство"),
            ("paragraph", "Современная форма философии всеединства, учитывающая многообразие и эволюцию бытия."),
            ("heading", "Этические принципы"),
            ("paragraph", "Универсальность, синтез, целостность, развитие, ответственность."),
        ],
    },
    "codex": {
        "title": "Интегральный кодекс",
        "preamble": "<p>Интегральный кодекс представляет собой философскую систему, соединяющую принципы универсальности и строгости на пути развития идей философии всеединства.</p>",
        "articles": [
            {"type": "article", "value": {"title": "Теоретическая часть", "content": "<p>Основы метафизики и онтологии. Категории бытия, сознания, значения.</p>"}},
            {"type": "article", "value": {"title": "Этическая часть", "content": "<p>Принципы поведения и синтеза. Универсализация этических норм.</p>"}},
            {"type": "article", "value": {"title": "Прикладная часть", "content": "<p>Практическое применение идей в науке, образовании и практике.</p>"}},
        ],
    },
    "dictionary": {
        "title": "Словарь интегральной философии",
        "terms": [
            {"type": "term", "value": {"word": "Интегральная философия", "definition": "<p>Направление мысли, стремящееся к синтезу всех уровней познания — научного, философского, художественного и духовного.</p>", "etymology": "от лат. integratio — восстановление, целостность", "related_terms": ["Неовсеединство", "Синтез"]}},
            {"type": "term", "value": {"word": "Неовсеединство", "definition": "<p>Современное развитие идеи всеединства: признание многообразия при сохранении фундаментального единства бытия.</p>", "etymology": "от рус. нео- + всеединство", "related_terms": ["Интегральная философия"]}},
            {"type": "term", "value": {"word": "Синтез", "definition": "<p>Метод соединения противоположностей в более широкое, непротиворечивое целое.</p>", "etymology": "от греч. σύνθεσις", "related_terms": ["Интегральная философия"]}},
        ],
    },
    "institute": {
        "introduction": "<p>Институт интегральной науки (ИИН). Создан 4 января 2025 года участниками сообщества «Интегральная философия».</p>",
        "subjects": [
            ("ethics", "Этика", "Моральные принципы и этические системы интегрального подхода.", "intermediate"),
            ("word", "Словесность", "Литература, риторика, языкознание как часть интегрального образования.", "beginner"),
            ("math", "Математика", "Математические основы философии и методы формализации.", "advanced"),
            ("hist", "История", "История идей всеединства и интегрального мышления.", "intermediate"),
            ("law", "Право", "Правовые основы общества развития и интегрального права.", "intermediate"),
        ],
    },
    "journal": {
        "title": "Журнал «Интегральная философия»",
        "volume": "№ 15",
        "publication_date": datetime.date(2024, 6, 1),
        "description": "<p>Научный журнал «Интегральная философия» предоставляет площадку для выражения своих позиций и теоретических разработок участникам Интегрального сообщества.</p>",
        "articles": [
            {"type": "article", "value": {"title": "Интегральный метод в исследованиях", "authors": "Иванов А., Петрова Б.", "abstract": "Методологическая рамка для междисциплинарных работ.", "url": "https://allunity.ru/journal.shtml"}},
            {"type": "article", "value": {"title": "Этика развития", "authors": "Сидоров В.", "abstract": "Нравственные основания принципов неовсеединства.", "url": "https://allunity.ru/journal.shtml"}},
        ],
    },
    "library": {
        "title": "Библиотека",
        "description": "<p>Ресурсы по интегральной философии и смежным областям. Научные работы, учебные материалы, периодика.</p>",
        "resources": [
            {"type": "resource", "value": {"title": "Всеединство: anthology", "author": "AllUnity", "resource_type": "Подборка", "url": "https://allunity.ru/library.shtml", "description": "Собрание ключевых текстов по теме всеединства."}},
            {"type": "resource", "value": {"title": "Журнал «Интегральная философия»", "author": "AllUnity", "resource_type": "Журнал", "url": "https://allunity.ru/journal.shtml", "description": "Периодическое издание сообщества."}},
        ],
    },
    "emblem": {
        "title": "Эмблема сообщества",
        "symbolism": "<p>Эмблема интегрального сообщества отражает основные принципы интегральной философии: единство в многообразии, синтез противоположностей и стремление к целостному познанию реальности.</p>",
        "history_of_creation": "<p>Геометрические элементы эмблемы символизируют различные уровни бытия и их взаимосвязь в рамках интегрального подхода.</p>",
        "usage_guidelines": "<p>Эмблема используется в официальных материалах сообщества, публикациях и образовательных программах.</p>",
    },
    "history": {
        "title": "История сообщества",
        "timeline": [
            {"type": "event", "value": {"date": "2015-01-01", "title": "Основание сообщества", "description": "<p>Начало систематической работы по консолидации направлений интегральной философии.</p>"}},
            {"type": "event", "value": {"date": "2018-01-01", "title": "Создание ИИН", "description": "<p>Объединение исследовательских программ под эгидой Института интегральной науки.</p>"}},
            {"type": "event", "value": {"date": "2021-01-01", "title": "Периодическое издание", "description": "<p>Запуск журнала «Интегральная философия».</p>"}},
            {"type": "event", "value": {"date": "2025-01-01", "title": "Цифровая платформа", "description": "<p>Обновление сайта и переход на современный CMS.</p>"}},
        ],
    },
    "school": {
        "title": "Школы интегральной философии",
        "admission_requirements": "<p>Программы открыты для исследователей, студентов и всех, кто интересуется интегральным подходом.</p>",
        "curriculum_overview": "<p>Комбинация философских, научных и практических дисциплин, направленная на целостное развитие.</p>",
        "programs": [
            {"type": "program", "value": {"name": "Основы интегральной философии", "duration": "1 год", "description": "<p>Введение в принципы всеединства и методы синтеза.</p>", "subjects": ["Этика", "Математика", "Словесность"]}},
            {"type": "program", "value": {"name": "Интегральная практика", "duration": "2 года", "description": "<p>Прикладные методы развития личности и преобразования мышления.</p>", "subjects": ["Этика", "Практика", "Диалог"]}},
        ],
    },
    "projects": [
        ("Неовсеединство", "active", "Современное развитие философии всеединства с использованием математических и логических методов."),
        ("Интегралика", "active", "Интегральный подход к образованию и развитию личности."),
        ("Единое знание", "planning", "Единая система знания across дисциплин."),
        ("Математизация философии", "active", "Формализация философских категорий средствами математики."),
        ("Интегральная медицина", "planning", "Целостный подход к здоровью и практике."),
    ],
    "news": [
        ("Создан Институт интегральной науки", "AllUnity", datetime.date(2025, 1, 4), "4 января 2025 года участниками сообщества «Интегральная философия» было создано общественное объединение «Институт интегральной науки» (ИИН). В рамках работы ИИН были организованы научные лаборатории по различным направлениям интегральной науки."),
        ("Готовится новый выпуск журнала", "AllUnity", datetime.date(2024, 12, 15), "Редакция готовит очередной номер журнала «Интегральная философия»."),
        ("Обновление сайта сообщества", "AllUnity", datetime.date(2024, 11, 20), "Переход на новый CMS-движок для улучшения доступности материалов."),
        ("Развитие проекта «Математизация философии»", "AllUnity", datetime.date(2024, 10, 5), "Формализация философских категорий средствами математики продолжается."),
    ],
    "discussions": [
        ("Смысл интегрального подхода", "Анна", "Как практический интегральный метод сочетается с повседневными решениями?"),
        ("Синтез науки и философии", "Борис", "Нужна ли формальная математизация философии для реального диалога?"),
        ("Методология исследований ИИН", "Мария", "Какие протоколы используются в лабораториях сообщества?"),
    ],
}


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
        self.create_journal()
        self.create_library()
        self.create_search()
        self.stdout.write(self.style.SUCCESS("Migration completed."))

    def clear_children(self):
        """Remove any previously-created pages under root so the run is repeatable."""
        if self.dry_run:
            return
        for child in self.root.get_children():
            child.delete()
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
        page = model(slug=slug, show_in_menus=True, live=True, first_published_at=timezone.now(), **fields)
        parent.add_child(instance=page)
        return page

    def create_home(self):
        self.stdout.write("Creating HomePage...")
        home = self.upsert(
            self.root, HomePage, "home",
            title="Интегральное сообщество",
            hero_title=REAL_CONTENT["home"]["hero_title"],
            hero_subtitle=REAL_CONTENT["home"]["hero_subtitle"],
            body=self.to_stream(REAL_CONTENT["home"]["body"]),
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
            title="Институт интегральной науки",
            introduction=REAL_CONTENT["institute"]["introduction"],
        )
        if not inst or self.dry_run:
            return
        for slug, title, desc, level in REAL_CONTENT["institute"]["subjects"]:
            self.upsert(
                inst, SubjectPage, slug,
                title=title, search_description=desc, difficulty_level=level,
                subject_code=slug.upper(),
                introduction=f"<p>{desc}</p>",
                curriculum=[{"type": "module", "value": {"title": title, "description": f"<p>{desc}</p>", "lessons": [{"type": "lesson_title", "value": "Введение"}, {"type": "lesson_content", "value": f"<p>{desc}</p>"}]}}],
            )

    def create_news(self):
        self.stdout.write("Creating News...")
        self.upsert(self.home_page, NewsIndexPage, "news", title="Новости")

    def create_projects(self):
        self.stdout.write("Creating Projects...")
        self.upsert(self.home_page, ProjectIndexPage, "projects",
                    title="Проекты", introduction="<p>Исследовательские проекты сообщества.</p>")

    def seed_news(self):
        self.stdout.write("Seeding News entries...")
        news_index = NewsIndexPage.objects.live().first()
        if not news_index or self.dry_run:
            return
        for i, (title, author, date, body) in enumerate(REAL_CONTENT["news"], 1):
            slug = f"news-{i}"
            self.upsert(
                news_index, NewsPage, slug,
                title=title, author=author, date=date, summary=title,
                body=[("paragraph", f"<p>{body}</p>")],
            )

    def seed_projects(self):
        self.stdout.write("Seeding Project entries...")
        proj_index = ProjectIndexPage.objects.live().first()
        if not proj_index or self.dry_run:
            return
        for i, (name, status, desc) in enumerate(REAL_CONTENT["projects"], 1):
            slug = f"project-{i}"
            self.upsert(
                proj_index, ProjectPage, slug,
                title=name, project_status=status,
                overview=RichText(f"<p>{desc}</p>"),
            )

    def create_manifest(self):
        self.stdout.write("Creating Manifest...")
        self.upsert(
            self.home_page, ManifestPage, "manifest",
            title=REAL_CONTENT["manifest"]["title"],
            introduction=REAL_CONTENT["manifest"]["introduction"],
            body=self.to_stream(REAL_CONTENT["manifest"]["body"]),
        )

    def create_search(self):
        self.stdout.write("Creating Search page...")
        self.upsert(self.home_page, SearchPage, "search", title="Поиск",
                    intro="<p>Поиск по материалам сообщества.</p>")

    def create_discussions(self):
        self.stdout.write("Creating Discussions...")
        idx = self.upsert(self.home_page, DiscussionIndexPage, "discussions", title="Дискуссии",
                          rules="<p>Правила обсуждений сообщества AllUnity.</p>")
        if not idx or self.dry_run:
            return
        for i, (topic, author, text) in enumerate(REAL_CONTENT["discussions"], 1):
            self.upsert(idx, DiscussionPage, f"thread-{i}",
                        title=f"Тред {i}", topic=topic, author=author,
                        initial_post=f"<p>{text}</p>", is_pinned=(i == 1), is_locked=False)

    def create_journal(self):
        self.stdout.write("Creating Journal...")
        self.upsert(self.home_page, JournalPage, "journal",
                    title=REAL_CONTENT["journal"]["title"],
                    volume=REAL_CONTENT["journal"]["volume"],
                    publication_date=REAL_CONTENT["journal"]["publication_date"],
                    description=REAL_CONTENT["journal"]["description"],
                    articles=REAL_CONTENT["journal"]["articles"])

    def create_library(self):
        self.stdout.write("Creating Library...")
        self.upsert(self.home_page, LibraryPage, "library",
                    title=REAL_CONTENT["library"]["title"],
                    description=REAL_CONTENT["library"]["description"],
                    resources=REAL_CONTENT["library"]["resources"])

    def create_content_pages(self):
        self.stdout.write("Creating content pages...")
        self.upsert(self.home_page, CodexPage, "codex",
                    title=REAL_CONTENT["codex"]["title"],
                    preamble=REAL_CONTENT["codex"]["preamble"],
                    articles=REAL_CONTENT["codex"]["articles"])
        self.upsert(self.home_page, DictionaryPage, "dictionary", title=REAL_CONTENT["dictionary"]["title"],
                    terms=REAL_CONTENT["dictionary"]["terms"])
        self.upsert(self.home_page, SchoolPage, "school",
                    title=REAL_CONTENT["school"]["title"],
                    admission_requirements=REAL_CONTENT["school"]["admission_requirements"],
                    curriculum_overview=REAL_CONTENT["school"]["curriculum_overview"],
                    programs=REAL_CONTENT["school"]["programs"])
        self.upsert(self.home_page, HistoryPage, "history", title=REAL_CONTENT["history"]["title"],
                    timeline=REAL_CONTENT["history"]["timeline"])
        self.upsert(self.home_page, EmblemPage, "emblem",
                    title=REAL_CONTENT["emblem"]["title"],
                    symbolism=REAL_CONTENT["emblem"]["symbolism"],
                    history_of_creation=REAL_CONTENT["emblem"]["history_of_creation"],
                    usage_guidelines=REAL_CONTENT["emblem"]["usage_guidelines"])

    def to_stream(self, blocks):
        out = []
        for kind, value in blocks:
            if kind == "heading":
                out.append(("heading", value))
            else:
                out.append(("paragraph", value))
        return out
