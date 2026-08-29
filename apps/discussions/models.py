from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from apps.core.models import BasePage


class DiscussionIndexPage(BasePage):
    rules = RichTextField("Правила обсуждений", blank=True)
    content_panels = Page.content_panels + [FieldPanel("rules")]


class DiscussionPage(BasePage):
    topic = models.CharField("Тема обсуждения", max_length=200)
    author = models.CharField("Автор", max_length=100)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    is_pinned = models.BooleanField("Закреплено", default=False)
    is_locked = models.BooleanField("Заблокировано", default=False)
    initial_post = RichTextField("Начальное сообщение")
    content_panels = Page.content_panels + [
        FieldPanel("topic"), FieldPanel("author"), FieldPanel("is_pinned"),
        FieldPanel("is_locked"), FieldPanel("initial_post"),
    ]
    parent_page_types = ["DiscussionIndexPage"]
