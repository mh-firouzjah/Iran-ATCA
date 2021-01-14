from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin
from sorl.thumbnail.admin import AdminImageMixin

from .models import Comment, Post, PostCategory, PostImages, Tags


class PostImagesInline(AdminImageMixin, admin.TabularInline):
    model = PostImages
    extra = 1
    # # from django.db import models as db_model
    # # from django.forms.widgets import FileInput
    # formfield_overrides = {
    #     db_model.ImageField: {'widget': FileInput(
    #         attrs={'class':
    #                'form-control',
    #                'required': True,
    #                })}}

    class Media:
        js = ('js/image_float.js', )


@admin.register(Post)
class PostAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    search_fields = ('title', 'body')
    list_display = ('title', 'slug', 'author', 'publish_jalali',
                    'status', 'public', 'international')
    list_display_links = ('title', 'slug', )
    list_editable = ('status', 'public', 'international')
    list_filter = ('status', 'created', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('author', 'categories', 'tags')
    date_hierarchy = 'publish'
    ordering = ('status', 'publish', 'public')
    exclude = ('search_vector',)
    inlines = (PostImagesInline, )

    def publish_jalali(self, obj):
        return datetime2jalali(obj.publish).strftime('%y/%m/%d، ساعت %H:%M')
    publish_jalali.admin_order_field = 'publish'
    publish_jalali.short_description = _('publish')


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name_en', 'name_fa')
    list_display = ('name_en', 'name_fa', 'icon')
    list_display_links = ('name_en', 'name_fa', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    # readonly_fields = ('slug', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)

        if any(item in search_term for item in ",،"):
            search_term = search_term.replace(',', '').replace('،', '')
            new_cat, created = PostCategory.objects.get_or_create(name=search_term)
            if created:
                queryset = PostCategory.objects.filter(name=search_term)
        return queryset, use_distinct


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'replied',
                    'created', 'active', 'public', 'publish', )
    list_display_links = ('user', 'post', 'replied', )
    search_fields = ('post__title', 'user__get_full_name', 'content')
    autocomplete_fields = ('post', 'user', 'replied')

    list_editable = ('active', 'public',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ('name_en', 'name_fa', )
    list_display = ('name_en', 'name_fa', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)

        if any(item in search_term for item in ",،"):
            search_term = search_term.replace(',', '').replace('،', '')
            new_cat, created = Tags.objects.get_or_create(name=search_term)
            if created:
                queryset = Tags.objects.filter(name=search_term)
        return queryset, use_distinct
