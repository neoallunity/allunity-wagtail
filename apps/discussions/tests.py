from django.test import TestCase, Client
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page, Site
from apps.discussions.models import DiscussionIndexPage, DiscussionPage


class DiscussionPageTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        self.idx = DiscussionIndexPage(title="Дискуссии", slug="test-disc")
        self.root.add_child(instance=self.idx)
        self.disc = DiscussionPage(
            title="Тред 1", slug="test-thread",
            topic="О смысле вселенной", author="Аноним",
            initial_post="<p>Первое сообщение</p>",
        )
        self.idx.add_child(instance=self.disc)

    def test_can_create(self):
        self.assertCanCreateAt(DiscussionIndexPage, DiscussionPage)

    def test_discussion_fields(self):
        self.assertEqual(self.disc.topic, "О смысле вселенной")
        self.assertEqual(self.disc.author, "Аноним")

    def test_discussion_renders(self):
        Site.objects.get_or_create(
            hostname="testserver", port=80,
            defaults={"root_page": self.root, "site_name": "AllUnity"})
        r = self.client.get(self.disc.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Первое сообщение")
