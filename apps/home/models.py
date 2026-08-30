from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search.models import Query
from apps.core.models import BasePage


class SearchPage(BasePage):
    max_count = 1
    intro = RichTextField("Введение", blank=True)
    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from wagtail.search.backends import get_search_backend
        query = request.GET.get("q", "").strip()
        results = []
        if query:
            sbackend = get_search_backend()
            results = sbackend.search(query, Page.objects.live().public().specific())
            try:
                Query.get(query).add_hit()
            except Exception:
                pass
        context["search_query"] = query
        context["search_results"] = results
        return context


class HomePage(BasePage):
    hero_title = models.CharField("Заголовок героя", max_length=200)
    hero_subtitle = models.TextField("Подзаголовок героя", max_length=500)
    hero_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    body = StreamField([
        ("heading", blocks.CharBlock(classname="title")),
        ("paragraph", blocks.TextBlock()),
        ("image", ImageChooserBlock()),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("body"),
    ]
