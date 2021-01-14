from modeltranslation.translator import TranslationOptions, register

from .models import Notification, User


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'description', 'story')



@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ('event', 'content', )
