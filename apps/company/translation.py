from modeltranslation.translator import TranslationOptions, register

from .models import Company, CompanySocialLink, Timetable, UsefulLink


@register(Company)
class CompanyTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'long_description',
              'address', 'footer_description', 'address')


@register(UsefulLink)
class UsefulLinkTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(Timetable)
class TimetableTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(CompanySocialLink)
class CompanySocialLinkTranslationOptions(TranslationOptions):
    fields = ('title',)
