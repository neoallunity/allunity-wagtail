from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, FieldPanel
from wagtail.images.models import Image
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from apps.core.models import BasePage


class NewsIndexPage(BasePage):
    max_count = 1
    content_panels = Page.content_panels + []


class NewsPage(BasePage):
    date = models.DateField("Дата публикации", null=True, blank=True,
        help_text="Дата публикации новости (задаётся вручную).")
    author = models.CharField("Автор", max_length=100)
    summary = models.CharField("Краткое описание", max_length=300, blank=True,
        help_text="Отображается в списке новостей и в поиске.")
    featured_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    body = StreamField([
        ("paragraph", blocks.TextBlock()),
        ("image", ImageChooserBlock()),
        ("quote", blocks.BlockQuoteBlock()),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel("date"), FieldPanel("author"), FieldPanel("summary"),
        FieldPanel("featured_image"), FieldPanel("body"),
    ]
    parent_page_types = ["NewsIndexPage"]
