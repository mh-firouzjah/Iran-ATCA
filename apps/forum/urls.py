from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path("", views.ForumListView.as_view(), name="forum_list"),
    path('search/', views.ForumListView.as_view(), name='forum_search'),
    path('<int:pk>/join/<str:token>/', views.join_forum_and_redirect, name="join_room"),
    path('<int:pk>/', views.ForumDetailView.as_view(), name='room'),

    path('add-chat/<int:chat_id>/', views.add_chat, name='add_chat'),
    path('delete-chat/<int:chat_id>/', views.delete_chat, name='delete_chat'),
    path('edit-chat/<int:chat_id>/', views.edit_chat, name='edit_chat'),
]
