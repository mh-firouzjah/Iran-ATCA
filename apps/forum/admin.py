from django.contrib import admin

from .models import Chat, Forum


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'invite_link', )
    autocomplete_fields = ('admin',)
    filter_horizontal = ('members', )
    readonly_fields = ('invite_link', )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    search_fields = ('name__get_full_name', )
    list_display = ('user', 'forum', 'reply', 'created', 'updated',)
