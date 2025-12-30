from django.contrib.sitemaps import Sitemap
from posts.models import Post
from django.urls import reverse


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    i18n = True
    alternates = True

    def items(self):
        return ['home', 'all-posts', 'articles', 'tutorials']

    def location(self, item):
        if isinstance(item, tuple):
            url_name, kwargs = item
            return reverse(url_name, kwargs=kwargs)
        else:
            return reverse(item)


class PostDetailSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    i18n = True
    alternates = True

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at
