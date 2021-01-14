from modeltranslation.translator import TranslationOptions, register

from .models import Document, DocumentCategory


@register(Document)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content')


@register(DocumentCategory)
class PostCategoryTranslationOptions(TranslationOptions):
    fields = ('title', )
