from django.core.management.base import BaseCommand
from django.conf import settings
from wagtail.models import Site, Page
from apps.home.models import HomePage
from apps.institute.models import InstituteIndexPage, SubjectPage
from apps.news.models import NewsIndexPage
from apps.projects.models import ProjectIndexPage
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = "Migrate content from old AllUnity SHTML site into Wagtail."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Run without writing.")

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        root = Page.objects.get(depth=1).specific
        self.create_home(root)
        self.create_institute(root)
        self.create_news(root)
        self.create_projects(root)
        self.stdout.write(self.style.SUCCESS("Migration completed."))

    def create_home(self, root):
        self.stdout.write("Creating HomePage...")
        if self.dry_run:
            return
        HomePage.objects.all().delete()
        home = HomePage(
            title="AllUnity — Интегральная философия и наука",
            slug="home",
            hero_title="Добро пожаловать в AllUnity",
            hero_subtitle="Философия, наука и искусство в едином целом",
            body=self.parse_streamfield(self.fetch("https://allunity.ru/index.shtml")),
        )
        root.add_child(instance=home)
        site = Site.objects.get(is_default_site=True)
        site.root_page = home
        site.save()

    def create_institute(self, root):
        self.stdout.write("Creating Institute...")
        if self.dry_run:
            return
        inst = InstituteIndexPage(title="Институт", slug="institute",
                                  introduction="<p>Образовательные программы AllUnity</p>")
        root.add_child(instance=inst)
        for slug, title, desc in [
            ("etics", "Этика", "Моральные принципы и этические системы"),
            ("word", "Словесность", "Литература, риторика, языкознание"),
            ("math", "Математика", "Математические основы философии"),
            ("hist", "История", "История идей"),
            ("law", "Право", "Правовые основы общества"),
        ]:
            SubjectPage(title=title, slug=slug, search_description=desc,
                        difficulty_level="intermediate",
                        introduction=f"<p>{desc}</p>",
                        curriculum=self.parse_curriculum(self.fetch(f"https://allunity.ru/{slug}.shtml"))).save()

    def create_news(self, root):
        self.stdout.write("Creating News...")
        if not self.dry_run:
            NewsIndexPage(title="Новости", slug="news").save()

    def create_projects(self, root):
        self.stdout.write("Creating Projects...")
        if not self.dry_run:
            ProjectIndexPage(title="Проекты", slug="projects",
                             introduction="<p>Исследовательские проекты AllUnity</p>").save()

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
