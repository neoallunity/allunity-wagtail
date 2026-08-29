from django.test import TestCase, Client
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page, Site
from apps.home.models import HomePage
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
