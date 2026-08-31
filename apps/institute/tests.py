from django.test import TestCase, Client
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page, Site
from apps.institute.models import InstituteIndexPage, SubjectPage, LaboratoryPage


class InstitutePageTests(WagtailPageTests):
    def setUp(self):
        self.root = Page.objects.get(depth=1)
        Site.objects.get_or_create(
            hostname="testserver", port=80,
            defaults={"root_page": self.root, "site_name": "AllUnity"},
        )
        self.idx = InstituteIndexPage(title="Институт", slug="inst")
        self.root.add_child(instance=self.idx)
        self.subj = SubjectPage(
            title="Этика", slug="ethics", subject_code="ETICS",
            difficulty_level="beginner", introduction="<p>intro</p>",
            curriculum=[],
        )
        self.idx.add_child(instance=self.subj)
        self.lab = LaboratoryPage(
            title="Лаб", slug="lab", lab_type="other",
            equipment=[], experiments=[],
        )
        self.idx.add_child(instance=self.lab)

    def test_institute_renders(self):
        r = self.client.get(self.idx.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Институт")

    def test_subject_renders(self):
        r = self.client.get(self.subj.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Этика")

    def test_laboratory_renders(self):
        r = self.client.get(self.lab.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Лаб")

    def test_nested_pages(self):
        self.assertTrue(self.subj.get_parent().id, self.idx.id)
        self.assertTrue(self.lab.get_parent().id, self.idx.id)
