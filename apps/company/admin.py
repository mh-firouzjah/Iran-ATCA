from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import (Company, CompanySocialLink, ContactUs, Timetable,
                     UsefulLink)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'darken_logo')
    list_display_links = ('name', 'email', )
    list_editable = ('darken_logo', )
    autocomplete_fields = ('social_links', )

    def has_add_permission(self, request, obj=None):
        if Company.objects.count() > 0:
            return False
        return super().has_add_permission(request)


@admin.register(UsefulLink)
class UsefulLinkAdmin(admin.ModelAdmin):
    search_fields = ('title', 'url')
    list_display = ('title', 'url')
    list_display_links = ('title', 'url')


@admin.register(CompanySocialLink)
class CompanySocialLinkAdmin(admin.ModelAdmin):
    search_fields = ('url', )
    list_display = ('url', 'show_icon')

    def show_icon(self, obj):
        return mark_safe(obj.icon)
    show_icon.short_description = _('Icon')


@admin.register(Timetable)
class TimetableAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    search_fields = ('name', 'date', 'get_description', 'content',)
    list_display = ('name', 'date', 'get_description', 'public')
    list_editable = ('date', 'public')

    def get_description(self, obj):
        return mark_safe(obj.description)


@admin.register(ContactUs)
class ContactUsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_jalali', 'client_ip')


    def created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%y/%m/%d، ساعت %H:%M')
    created_jalali.admin_order_field = 'created'
    created_jalali.short_description = _('Created')
