from django.test import TestCase, Client
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page, Site
from apps.projects.models import ProjectIndexPage, ProjectPage


class ProjectPageTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        Site.objects.get_or_create(
            hostname="testserver", port=80,
            defaults={"root_page": self.root, "site_name": "AllUnity"},
        )
        self.idx = ProjectIndexPage(title="Проекты", slug="proj")
        self.root.add_child(instance=self.idx)
        self.proj = ProjectPage(
            title="Проект А", slug="proj-a",
            project_status="active", overview="<p>обзор</p>",
            objectives=[], publications=[],
        )
        self.idx.add_child(instance=self.proj)

    def test_project_renders(self):
        r = self.client.get(self.proj.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Проект А")

    def test_project_status(self):
        self.assertEqual(self.proj.project_status, "active")

    def test_index_renders(self):
        r = self.client.get(self.idx.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Проекты")
