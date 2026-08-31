from django.test import TestCase, Client
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page, Site
from apps.home.models import HomePage, SearchPage
from apps.institute.models import InstituteIndexPage, SubjectPage
from apps.news.models import NewsIndexPage, NewsPage
from apps.projects.models import ProjectIndexPage, ProjectPage
from apps.discussions.models import DiscussionIndexPage, DiscussionPage
from apps.content.models import ManifestPage, CodexPage, DictionaryPage, SchoolPage, HistoryPage, EmblemPage


class HomePageTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        from wagtail.models import Site
        Site.objects.get_or_create(
            hostname="testserver", port=80, defaults={"root_page": self.root, "site_name": "AllUnity"}
        )
        self.home = HomePage(title="Test Home", slug="test-home", hero_title="T", hero_subtitle="S")
        self.root.add_child(instance=self.home)

    def test_can_create_home_page(self):
        self.assertCanCreateAt(Page, HomePage)

    def test_home_renders(self):
        r = self.client.get(self.home.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "T")


class InstitutePageTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        self.inst = InstituteIndexPage(title="Inst", slug="test-inst")
        self.root.add_child(instance=self.inst)
        self.subj = SubjectPage(title="Subj", slug="test-subj", subject_code="TS",
                                difficulty_level="beginner", introduction="<p>intro</p>")
        self.inst.add_child(instance=self.subj)

    def test_can_create_institute(self):
        self.assertCanCreateAt(Page, InstituteIndexPage)
        self.assertCanCreateAt(InstituteIndexPage, SubjectPage)

    def test_subject_content(self):
        self.assertEqual(self.subj.subject_code, "TS")


class NewsPageTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        self.idx = NewsIndexPage(title="News", slug="test-news")
        self.root.add_child(instance=self.idx)
        self.np = NewsPage(title="N", slug="test-n", author="A")
        self.idx.add_child(instance=self.np)

    def test_news_author(self):
        self.assertEqual(self.np.author, "A")

    def test_news_date_autoset(self):
        self.assertIsNotNone(self.np.date)


class ProjectPageTests(WagtailPageTests):
    def test_can_create(self):
        self.assertCanCreateAt(ProjectIndexPage, ProjectPage)


class ContentPageTests(WagtailPageTests):
    def test_variants(self):
        for M in (ManifestPage, CodexPage, DictionaryPage, SchoolPage, HistoryPage, EmblemPage):
            self.assertCanCreateAt(Page, M)


class SEOTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.root = Page.objects.get(depth=1)
        from wagtail.models import Site
        Site.objects.get_or_create(
            hostname="testserver", port=80, defaults={"root_page": self.root, "site_name": "AllUnity"}
        )
        self.home = HomePage(title="SEO", slug="seo", seo_title="Custom",
                             search_description="desc", hero_title="h", hero_subtitle="s")
        self.root.add_child(instance=self.home)

    def test_seo_title(self):
        r = self.client.get(self.home.url)
        self.assertContains(r, "Custom")

    def test_sitemap(self):
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)


class SearchPageTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        Site.objects.get_or_create(
            hostname="testserver", port=80, defaults={"root_page": self.root, "site_name": "AllUnity"}
        )
        self.home = HomePage(title="H", slug="search-home", hero_title="h", hero_subtitle="s")
        self.root.add_child(instance=self.home)
        self.search = SearchPage(title="Поиск", slug="search")
        self.home.add_child(instance=self.search)
        self.search.save_revision().publish() if hasattr(self.search, "save_revision") else None
        self.home.save_revision().publish() if hasattr(self.home, "save_revision") else None

    def test_search_page_renders(self):
        r = self.client.get(self.search.url)
        self.assertEqual(r.status_code, 200)

    def test_search_query_returns_results(self):
        # A query matching the hero text should surface the home page
        r = self.client.get(self.search.url + "?q=AllUnity")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "AllUnity")


class AllPagesSmokeTest(WagtailPageTests):
    """e2e smoke: build the full page tree and assert every live page returns 200."""

    def setUp(self):
        self.root = Page.objects.get(depth=1)
        Site.objects.get_or_create(
            hostname="testserver", port=80,
            defaults={"root_page": self.root, "site_name": "AllUnity"})
        self.home = HomePage(title="Главная", slug="smoke-home",
                             hero_title="h", hero_subtitle="s",
                             body=[("paragraph", "<p>тело</p>")])
        self.root.add_child(instance=self.home)
        sections = [
            (InstituteIndexPage, "institute", "Институт"),
            (NewsIndexPage, "news", "Новости"),
            (ProjectIndexPage, "projects", "Проекты"),
            (ManifestPage, "manifest", "Манифест"),
            (DiscussionIndexPage, "discussions", "Дискуссии"),
            (CodexPage, "codex", "Кодекс"),
            (DictionaryPage, "dictionary", "Словарь"),
            (SchoolPage, "school", "Школа", {"admission_requirements": "<p>a</p>", "curriculum_overview": "<p>c</p>"}),
            (HistoryPage, "history", "История"),
            (EmblemPage, "emblem", "Эмблема", {"symbolism": "<p>s</p>", "history_of_creation": "<p>h</p>", "usage_guidelines": "<p>u</p>"}),
            (SearchPage, "search", "Поиск"),
        ]
        for item in sections:
            model, slug, title = item[0], item[1], item[2]
            kwargs = item[3] if len(item) > 3 else {}
            page = model(title=title, slug=slug, **kwargs)
            self.home.add_child(instance=page)
            page.save_revision().publish()
        # nested pages
        subj = SubjectPage(title="Этика", slug="smoke-etics", subject_code="ETICS",
                           difficulty_level="beginner", introduction="<p>i</p>")
        InstituteIndexPage.objects.child_of(self.home).first().add_child(instance=subj)
        subj.save_revision().publish()
        news = NewsPage(title="Новость", slug="smoke-news", author="А",
                        body=[("paragraph", "<p>n</p>")])
        NewsIndexPage.objects.child_of(self.home).first().add_child(instance=news)
        news.save_revision().publish()
        proj = ProjectPage(title="Проект", slug="smoke-proj", project_status="active",
                           overview="<p>o</p>")
        ProjectIndexPage.objects.child_of(self.home).first().add_child(instance=proj)
        proj.save_revision().publish()
        disc = DiscussionPage(title="Тред", slug="smoke-disc", topic="t", author="a",
                              initial_post="<p>d</p>")
        DiscussionIndexPage.objects.child_of(self.home).first().add_child(instance=disc)
        disc.save_revision().publish()
        self.home.save_revision().publish()

    def test_all_live_pages_return_200(self):
        client = Client()
        failures = []
        for page in Page.objects.live().specific():
            try:
                r = client.get(page.url)
            except Exception as e:
                failures.append((page.url, f"exc {e}"))
                continue
            if r.status_code != 200:
                failures.append((page.url, r.status_code))
        self.assertEqual(failures, [], msg=f"Non-200 pages: {failures}")

    def test_rss_and_sitemap(self):
        client = Client()
        self.assertEqual(client.get("/news/rss/").status_code, 200)
        self.assertEqual(client.get("/sitemap.xml").status_code, 200)
        self.assertEqual(client.get("/robots.txt").status_code, 200)
