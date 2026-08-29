from django.core.management.base import BaseCommand
from wagtail.models import Site, Page
from apps.home.models import HomePage
from apps.institute.models import InstituteIndexPage, SubjectPage
from apps.news.models import NewsIndexPage
from apps.projects.models import ProjectIndexPage
from apps.content.models import ManifestPage
from bs4 import BeautifulSoup


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
        self.create_manifest()
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
            existing.specific.save()
            return existing.specific
        page = model(slug=slug, **fields)
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
        if home and not self.dry_run:
            site, _ = Site.objects.get_or_create(
                is_default_site=True,
                defaults={"hostname": "localhost", "port": 80, "root_page": self.root, "site_name": "AllUnity"},
            )
            site.root_page = self.root
            site.save()

    def create_institute(self):
        self.stdout.write("Creating Institute...")
        inst = self.upsert(
            self.root, InstituteIndexPage, "institute",
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
        self.upsert(self.root, NewsIndexPage, "news", title="Новости")

    def create_projects(self):
        self.stdout.write("Creating Projects...")
        self.upsert(self.root, ProjectIndexPage, "projects",
                    title="Проекты", introduction="<p>Исследовательские проекты AllUnity</p>")

    def create_manifest(self):
        self.stdout.write("Creating Manifest...")
        self.upsert(
            self.root, ManifestPage, "manifest",
            title="Манифест AllUnity",
            introduction="<p>Интегральное видение будущего человечества и планеты.</p>",
            body=self.parse_streamfield(self.fetch("https://allunity.ru/manifest.shtml")),
        )

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
