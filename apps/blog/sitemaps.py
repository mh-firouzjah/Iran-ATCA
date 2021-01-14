from itertools import chain
from operator import attrgetter

from django.contrib.sitemaps import Sitemap

from apps.documents.models import Document

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    # this generates urls per language
    i18n = True

    def items(self):
        result_list = sorted(
            chain(Post.published.all(), Document.objects.active()),
            key=attrgetter('publish'))
        return result_list

    def lastmod(self, obj):
        return obj.updated
