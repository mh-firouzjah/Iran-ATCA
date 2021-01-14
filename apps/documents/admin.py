from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Document, DocumentCategory


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('uploaded_by', 'categories')

    fieldsets = (
        (_("Title"), {
            "fields": (
                "title",
            ),
        }),
        (_("Title translation"), {
            "fields": (
                'title_fa', 'title_en'
            ),
            'classes': ('collapse',),
        }),
        (_("Description"), {
            "fields": (
                "description",
            ),
        }),
        (_("Description translation"), {
            "fields": (
                'description_fa', 'description_en'
            ),
            'classes': ('collapse',),
        }),
        (_("Info"), {
            "fields": (
                "slug",
                "uploaded_by",
                "document_type",
                "categories",
                "cover",
                "document_file",
                "publish",
                "status",
            ),
        }),
        (_("Content"), {
            "fields": (
                "content",
            ),
        }),
        (_("Content translation"), {
            "fields": (
                'content_fa', 'content_en'
            ),
            'classes': ('collapse',),
        }),
    )



@ admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'total_documents')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title_en'].required = True
        return form
