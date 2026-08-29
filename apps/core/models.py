from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class BasePage(Page):
    """Базовая модель всех страниц: SEO + OG поля."""

    class Meta:
        abstract = True

    description = models.TextField("Описание", max_length=500, blank=True)
    keywords = models.CharField("Ключевые слова", max_length=200, blank=True)
    social_image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    canonical_url = models.URLField("Каноническая ссылка", blank=True)
    robots_noindex = models.BooleanField("Запретить индексацию", default=False)
    robots_nofollow = models.BooleanField("Запретить следование", default=False)
    og_title = models.CharField("OG заголовок", max_length=100, blank=True)
    og_description = models.TextField("OG описание", max_length=300, blank=True)
    twitter_card_type = models.CharField(
        "Тип Twitter карты", max_length=20,
        choices=[("summary", "Summary"), ("summary_large_image", "Summary Large Image")],
        default="summary_large_image",
    )

    promote_panels = Page.promote_panels + [
        FieldPanel("description"),
        FieldPanel("keywords"),
        FieldPanel("social_image"),
        FieldPanel("canonical_url"),
        FieldPanel("robots_noindex"),
        FieldPanel("robots_nofollow"),
        FieldPanel("og_title"),
        FieldPanel("og_description"),
        FieldPanel("twitter_card_type"),
    ]
