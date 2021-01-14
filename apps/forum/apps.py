from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ForumAppConfig(AppConfig):
    name = 'apps.forum'

    verbose_name = _('Forum')
    verbose_name_plural = _('Forums')
