#!/usr/bin/env python3
"""Update HomePage content directly via ORM."""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allunity.settings.production')
django.setup()

from django.utils import timezone
from wagtail.models import Page, Site
from apps.home.models import HomePage

root = Page.objects.get(depth=1)
existing = root.get_children().filter(slug="home").first()
if existing:
    existing.delete()
    Page.fix_tree()

home = HomePage(
    slug="home",
    title="Интегральное сообщество",
    hero_title="Интегральное сообщество",
    hero_subtitle="Консолидация всех конструктивных сил на основе принципов интегральной философии",
    show_in_menus=True, live=True, first_published_at=timezone.now(),
)
root.add_child(instance=home)
Page.fix_tree()

site = Site.objects.first()
if site:
    site.root_page = home
    site.save()

print("HomePage updated to 'Интегральное сообщество'")
