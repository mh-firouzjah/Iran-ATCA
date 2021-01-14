from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomSettingsAppConfig(AppConfig):
    name = 'apps.custom'
    verbose_name = _("Custom Settings")
    verbose_name_plural = _("Custom Settings")
