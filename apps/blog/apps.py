from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogAppConfig(AppConfig):
    name = 'apps.blog'
    verbose_name = _("Blog")
    verbose_name_plural = _("Blogs")
