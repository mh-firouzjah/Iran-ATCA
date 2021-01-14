from django.urls import path

from . import views

app_name = "documents"

urlpatterns = [
    path('',
         views.DocumentListView.as_view(), name='document_list'),

    path('search/',
         views.DocumentListView.as_view(), name='document_search'),

    path('by/<str:username>/',
         views.DocumentListView.as_view(), name='documents_by_author'),

    path('archive/<int:year>/<int:month>/',
         views.DocumentListView.as_view(), name='document_list_archive'),

    path('<int:year>/<int:month>/<int:day>/<str:slug>/',
         views.DocumentDetailView.as_view(), name='document_detail'),
]
