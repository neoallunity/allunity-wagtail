from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, FieldPanel
from wagtail.images.models import Image
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from apps.core.models import BasePage


class ManifestPage(BasePage):
    introduction = RichTextField("Введение", blank=True)
    body = StreamField([
        ("heading", blocks.CharBlock(classname="title")),
        ("paragraph", blocks.RichTextBlock()),
        ("quote", blocks.BlockQuoteBlock()),
        ("list", blocks.ListBlock(blocks.CharBlock(label="Пункт"))),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel("introduction"), FieldPanel("body")]


class CodexPage(BasePage):
    preamble = RichTextField("Преамбула", blank=True)
    articles = StreamField([
        ("article", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Заголовок статьи")),
            ("content", blocks.RichTextBlock("Содержание статьи")),
        ])),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel("preamble"), FieldPanel("articles")]


class DictionaryPage(BasePage):
    terms = StreamField([
        ("term", blocks.StructBlock([
            ("word", blocks.CharBlock(label="Термин")),
            ("definition", blocks.RichTextBlock("Определение")),
            ("etymology", blocks.TextBlock(label="Этимология", required=False)),
            ("related_terms", blocks.ListBlock(blocks.CharBlock(label="Связанный термин"), required=False)),
        ])),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel("terms")]


class SchoolPage(BasePage):
    admission_requirements = RichTextField("Требования для поступления")
    curriculum_overview = RichTextField("Обзор учебной программы")
    programs = StreamField([
        ("program", blocks.StructBlock([
            ("name", blocks.CharBlock(label="Название программы")),
            ("duration", blocks.CharBlock(label="Продолжительность")),
            ("description", blocks.RichTextBlock("Описание")),
            ("subjects", blocks.ListBlock(blocks.CharBlock(label="Предмет"))),
        ])),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel("admission_requirements"), FieldPanel("curriculum_overview"), FieldPanel("programs"),
    ]


class HistoryPage(BasePage):
    timeline = StreamField([
        ("event", blocks.StructBlock([
            ("date", blocks.DateBlock(label="Дата")),
            ("title", blocks.CharBlock(label="Событие")),
            ("description", blocks.RichTextBlock("Описание")),
            ("image", ImageChooserBlock(required=False)),
        ])),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel("timeline")]


class EmblemPage(BasePage):
    emblem_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name="+")
    symbolism = RichTextField("Символизм эмблемы")
    history_of_creation = RichTextField("История создания")
    usage_guidelines = RichTextField("Правила использования")
    content_panels = Page.content_panels + [
        FieldPanel("emblem_image"), FieldPanel("symbolism"),
        FieldPanel("history_of_creation"), FieldPanel("usage_guidelines"),
    ]
