from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('feed/', LatestPostsFeed(), name='post_feed'),

    # post views
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.PostListView.as_view(), name='post_search'),

    path('written-by/<str:username>/',
         views.PostListView.as_view(), name='posts_by_author'),

    path('archive/<int:year>/<int:month>/',
         views.PostListView.as_view(), name='post_list_archive'),

    path('<int:year>/<int:month>/<int:day>/<str:slug>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    path('add-comment/<int:post_id>/<int:comment_id>/',
         views.add_comment, name='add_comment')
]
