import apps.users.views as users_views
from apps.blog.sitemaps import PostSitemap
from django.conf import settings
# from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

sitemaps = {
    'posts': PostSitemap,
}


admin.autodiscover()


last_modified_date = timezone.now()

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('settings/', users_views.settings, name='settings'),
    path('settings/password/', users_views.password, name='password'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    # path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]

urlpatterns += i18n_patterns(
    path('avatar/', include('avatar.urls')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('forum/', include('apps.forum.urls', namespace='forum')),
    path('documents/', include('apps.documents.urls', namespace='documents')),
    path('custom/', include('apps.custom.urls', namespace='custom')),
    path('', include('apps.company.urls', namespace='company')),
    path('admin/', admin.site.urls),
    prefix_default_language=True
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += i18n_patterns(
    path('jsi18n/',
         last_modified(lambda req, **kw: last_modified_date)
         (JavaScriptCatalog.as_view()),
         name='javascript-catalog'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = 'apps.custom.views.bad_request'
handler403 = 'apps.custom.views.permission_denied'
handler404 = 'apps.custom.views.page_not_found'
handler500 = 'apps.custom.views.server_error'
