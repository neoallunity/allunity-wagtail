from django.test import TestCase, Client
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page, Site
from apps.news.models import NewsIndexPage, NewsPage
from apps.news.feeds import NewsFeed


class NewsFeedTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        self.idx = NewsIndexPage(title="Новости", slug="test-news")
        self.root.add_child(instance=self.idx)
        self.np = NewsPage(title="Новость RSS", slug="test-nrss", author="Редакция",
                           body=[("paragraph", "<p>Тело новости для ленты</p>")])
        self.idx.add_child(instance=self.np)
        Site.objects.get_or_create(
            hostname="testserver", port=80,
            defaults={"root_page": self.root, "site_name": "AllUnity"})

    def test_feed_renders(self):
        r = self.client.get("/news/rss/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"].split(";")[0], "application/rss+xml")
        self.assertContains(r, "Новость RSS")
        self.assertContains(r, "Тело новости для ленты")

    def test_feed_items_count(self):
        feed = NewsFeed()
        items = list(feed.items())
        self.assertIn(self.np, items)
