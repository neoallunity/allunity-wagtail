from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /django-admin/",
        "Allow: /",
        "Sitemap: https://allunity.ru/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
