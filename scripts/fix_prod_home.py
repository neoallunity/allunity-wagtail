#!/usr/bin/env python3
"""Middleware-level fix: update home page content directly via SQL on each deploy."""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'allunity.settings.production')
django.setup()

from django.db import connection
# Directly update via SQL to bypass ORM/migration issues
with connection.cursor() as cursor:
    cursor.execute("""
        UPDATE home_homepage 
        SET hero_title = 'Интегральное сообщество',
            hero_subtitle = 'Консолидация всех конструктивных сил на основе принципов интегральной философии'
        WHERE page_ptr_id IN (
            SELECT id FROM wagtailcore_page WHERE slug = 'home' AND depth > 1
        )
    """)
    cursor.execute("""
        UPDATE wagtailcore_page 
        SET title = 'Интегральное сообщество' 
        WHERE slug = 'home' AND depth > 1
    """)
    print("Direct SQL update applied!")

# Verify
from wagtail.models import Page
home = Page.objects.filter(slug="home").first()
if home:
    specific = home.specific
    print(f"hero_title = {specific.hero_title}")
