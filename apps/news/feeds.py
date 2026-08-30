from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from apps.news.models import NewsPage


class NewsFeed(Feed):
    title = "Новости AllUnity"
    link = "/news/"
    description = "Последние новости Интегрального сообщества AllUnity."
    feed_type = Rss201rev2Feed

    def items(self):
        return NewsPage.objects.live().order_by("-date")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # Render the first paragraph of the body as the description.
        for block in item.body:
            if block.block_type == "paragraph" and block.value:
                return block.value
        return item.search_description or ""

    def item_link(self, item):
        return item.url

    def item_pubdate(self, item):
        return item.date
