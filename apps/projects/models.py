from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, FieldPanel
from wagtail import blocks
from apps.core.models import BasePage


class ProjectIndexPage(BasePage):
    introduction = RichTextField("Введение в проекты", blank=True)
    content_panels = Page.content_panels + [FieldPanel("introduction")]


class ProjectPage(BasePage):
    project_status = models.CharField("Статус проекта", max_length=20,
        choices=[("planning", "Планирование"), ("active", "Активный"),
                 ("completed", "Завершенный"), ("on_hold", "Приостановлен")])
    start_date = models.DateField("Дата начала", null=True, blank=True)
    end_date = models.DateField("Дата окончания", null=True, blank=True)
    overview = RichTextField("Обзор проекта")
    objectives = StreamField([("objective", blocks.CharBlock(label="Цель"))], blank=True, use_json_field=True)
    methodology = RichTextField("Методология", blank=True)
    results = RichTextField("Результаты", blank=True)
    publications = StreamField([
        ("publication", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Название публикации")),
            ("authors", blocks.CharBlock(label="Авторы")),
            ("journal", blocks.CharBlock(label="Журнал/Издание")),
            ("url", blocks.URLBlock(label="Ссылка", required=False)),
        ])),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel("project_status"), FieldPanel("start_date"), FieldPanel("end_date"),
        FieldPanel("overview"), FieldPanel("objectives"),
        FieldPanel("methodology"), FieldPanel("results"), FieldPanel("publications"),
    ]
    parent_page_types = ["ProjectIndexPage"]
