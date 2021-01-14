from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DocumentsAppConfig(AppConfig):
    name = 'apps.documents'
    verbose_name = _("Documents")
    verbose_name_plural = _("Documents")
