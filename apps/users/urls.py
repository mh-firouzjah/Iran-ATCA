from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls.base import reverse_lazy

from . import views as custom_views

app_name = "users"

management_patterns = [
    # Password Change
    path('password/change/',
         custom_views.CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # Password Reset
    path('password/reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('users:password_reset_done')
         ),
         name='password_reset'),
    path('password/reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]

urlpatterns = [
    path('login/', custom_views.CustomLoginView.as_view(),
         name='login'),
    path('logout/', custom_views.CustomLogOutView.as_view(),
         name='logout'),
    path('users/', custom_views.ATControllerListView.as_view(),
         name="user"),
    path('users/<int:pk>/',
         custom_views.UserDetailView.as_view(),
         name="user_detail"),
    path('users/atc/<int:pk>/',
         custom_views.ATControllerDetailView.as_view(),
         name="atc_user_detail"),
    path('signup/', custom_views.signup, name='signup'),
]

urlpatterns += management_patterns
