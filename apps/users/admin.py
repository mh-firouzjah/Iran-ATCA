import re

from avatar.models import Avatar
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from jalali_date.admin import ModelAdminJalaliMixin
from sorl.thumbnail.admin import AdminImageMixin

from . import models as custom_models
from . import views as custom_views

admin.autodiscover()
admin.site.login = custom_views.CustomLoginView.as_view()
admin.site.logout = custom_views.CustomLogOutView.as_view()


class AvatarInline(AdminImageMixin, admin.TabularInline):
    model = Avatar
    extra = 0

    class Media:
        css = {'all': ('css/image_float.css', )}


@admin.register(custom_models.User)
class CustomUserAdmin(UserAdmin):
    personal_fields = UserAdmin.fieldsets[1][1]['fields']
    extra_personal_fields = ('description', 'first_name_en',
                             'last_name_en', 'description_en',
                             'story', 'story_fa', 'story_en')
    UserAdmin.fieldsets[1][1]['fields'] = (*personal_fields, *extra_personal_fields)

    inlines = (AvatarInline, )

    # fieldsets = UserAdmin.fieldsets + (
    #     # ('Custom Field Heading', {'fields': ('custom_field',)}),
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     # ('Custom Field Heading', {'fields': ('custom_field',)}),

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request,
                                                            queryset, search_term)
        req = str(request.META.get('HTTP_REFERER'))
        req_for_change = re.search(r'airtrafficcontroller/\d+/change/', req)
        if 'airtrafficcontroller/add' in req:
            queryset = queryset.filter(atc_info=None)

        if req_for_change:
            pk = int(re.findall(r'\d+', req)[-1])
            queryset = queryset.filter(atc_info=pk)
        return queryset, use_distinct


@ admin.register(custom_models.Group)
class CustomGroupAdmin(GroupAdmin):
    horizontal_fields = ['permissions']


@ admin.register(custom_models.AirTrafficController)
class AirTrafficControllerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', )
    autocomplete_fields = ('user', )
    # def change_view(self, *args, **kwargs):
    #     self.form = super().get_form()
    #     self.form.exclude = 'user'
    #     return super().change_view(*args, **kwargs)


@admin.register(custom_models.SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    search_fields = ('link', 'user__username',
                     'user__first_name', 'user__last_name', 'media')


@admin.register(custom_models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    search_fields = ('users',)
    list_display = ('user', 'acknowledged', 'event', 'created')
    readonly_fields = ('acknowledged',)
    autocomplete_fields = ('user', )
