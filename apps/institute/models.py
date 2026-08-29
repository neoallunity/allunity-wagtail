from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from apps.core.models import BasePage


class InstituteIndexPage(BasePage):
    introduction = RichTextField("Введение", blank=True)
    content_panels = Page.content_panels + [FieldPanel("introduction")]


class SubjectPage(BasePage):
    subject_code = models.CharField("Код предмета", max_length=10)
    difficulty_level = models.CharField("Уровень сложности", max_length=20,
        choices=[("beginner", "Начинающий"), ("intermediate", "Средний"), ("advanced", "Продвинутый")])
    introduction = RichTextField("Введение в предмет")
    curriculum = StreamField([
        ("module", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Название модуля")),
            ("description", blocks.RichTextBlock("Описание модуля")),
            ("lessons", blocks.ListBlock(blocks.StructBlock([
                ("lesson_title", blocks.CharBlock(label="Урок")),
                ("lesson_content", blocks.RichTextBlock("Содержание")),
            ]))),
        ])),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel("subject_code"), FieldPanel("difficulty_level"),
        FieldPanel("introduction"), FieldPanel("curriculum"),
    ]


class LaboratoryPage(BasePage):
    lab_type = models.CharField("Тип лаборатории", max_length=50,
        choices=[("music", "Музыкальная"), ("physics", "Физическая"), ("other", "Другая")])
    equipment = StreamField([
        ("equipment_item", blocks.StructBlock([
            ("name", blocks.CharBlock(label="Название оборудования")),
            ("description", blocks.RichTextBlock("Описание")),
            ("image", ImageChooserBlock(required=False)),
        ])),
    ], blank=True, use_json_field=True)
    experiments = StreamField([
        ("experiment", blocks.StructBlock([
            ("title", blocks.CharBlock(label="Название эксперимента")),
            ("objective", blocks.TextBlock(label="Цель эксперимента")),
            ("methodology", blocks.RichTextBlock("Методология")),
            ("results", blocks.RichTextBlock("Ожидаемые результаты")),
        ])),
    ], blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel("lab_type"), FieldPanel("equipment"), FieldPanel("experiments"),
    ]
