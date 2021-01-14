from modeltranslation.translator import TranslationOptions, register

from .models import Post, PostCategory, Tags


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'descrip', 'body', )


@register(PostCategory)
class PostCategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Tags)
class TagsTranslationOptions(TranslationOptions):
    fields = ('name', )
