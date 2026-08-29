from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class QuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(label="Цитата")
    author = blocks.CharBlock(label="Автор", required=False)
    source = blocks.CharBlock(label="Источник", required=False)

    class Meta:
        template = "blocks/quote_block.html"
        icon = "openquote"
        label = "Цитата"


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок")
    text = blocks.RichTextBlock("Текст")
    button_text = blocks.CharBlock(label="Текст кнопки")
    button_url = blocks.URLBlock(label="Ссылка кнопки")
    background_color = blocks.ChoiceBlock(
        choices=[("blue", "Синий"), ("green", "Зеленый"), ("red", "Красный")]
    )

    class Meta:
        template = "blocks/cta_block.html"
        icon = "plus"
        label = "Призыв к действию"


class GalleryBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок галереи", required=False)
    images = blocks.ListBlock(blocks.StructBlock([
        ("image", ImageChooserBlock()),
        ("caption", blocks.CharBlock(label="Подпись", required=False)),
    ]))

    class Meta:
        template = "blocks/gallery_block.html"
        icon = "image"
        label = "Галерея"


class VideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок видео", required=False)
    video_url = blocks.URLBlock(label="URL видео (YouTube, Vimeo)")
    description = blocks.TextBlock(label="Описание", required=False)

    class Meta:
        template = "blocks/video_block.html"
        icon = "media"
        label = "Видео"


class TableBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Заголовок таблицы", required=False)
    table = blocks.TableBlock()

    class Meta:
        template = "blocks/table_block.html"
        icon = "table"
        label = "Таблица"
