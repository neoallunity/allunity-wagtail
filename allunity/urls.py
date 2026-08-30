from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps import views as sitemap_views
from apps.news.feeds import NewsFeed

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("sitemap.xml", sitemap_views.sitemap),
    path("news/rss/", NewsFeed(), name="news_rss"),
    path("", include(wagtail_urls)),
]

# robots.txt is optional (django-robots not required)
try:
    from django.urls import re_path
    import robots.views as _rv  # noqa
    urlpatterns.append(path("robots.txt", _rv.robots_txt, name="robots_txt"))
except Exception:
    pass

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
