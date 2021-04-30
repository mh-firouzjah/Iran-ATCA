# import logging
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AdminPasswordChangeForm,
                                       PasswordChangeForm)
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from social_django.models import UserSocialAuth

from apps.users.forms import (AirTrafficControllerForm, UserForm,
                              UserSocialMediaFormset)

from . import models


def user_is_atc(user):
    if user.is_anonymous:
        return False
    return models.AirTrafficController.objects.filter(user=user).exists()


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = _('Welcome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.username
        return context


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomLogOutView(LogoutView):
    template_name = 'registration/logged_out.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_message = _('Your password has been changed successfully')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, _('Good bye'))


class UserListView(ListView):
    model = models.User
    # inside template `object_list` or the lowercased version of
    # the model class’s name in this case `user`_list is refering to the list
    # you're able to choose any name using `context_object_name`

    paginate_by = 100  # -> this will create `page_obj` for pagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserDetailView(DetailView):
    model = models.User  # -> inside template `object` is refering to instace
    # context_object_name = 'user'  # -> now `user` is refering to instace
    template_name = 'users/user_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = None
        if self.object.atc_info:
            formset = UserSocialMediaFormset(instance=self.object.atc_info)
        context = self.get_context_data()
        context.update({
            'user_update_form': UserForm(instance=self.object, user=self.object),
            'atc_info_update_form': AirTrafficControllerForm(user=self.object),
            'formset': formset,
        })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        theres_error = False

        user_form = UserForm(request.POST, instance=self.object, user=self.object)
        atc_info = AirTrafficControllerForm(
            request.POST, instance=self.object, user=self.object)
        formset = UserSocialMediaFormset(request.POST, instance=self.object.atc_info)

        if user_form.is_valid():
            user_form.save()
        else:
            theres_error = True
        if atc_info.is_valid():
            atc_info.save()
        else:
            theres_error = True
        if formset.is_valid():
            formset.save()
        else:
            theres_error = True

        if theres_error:
            context = self.get_context_data()
            context.update({
                'user_update_form': user_form,
                'atc_info_update_form': atc_info,
                'formset': formset, })
            return render(request, self.template_name, context)
        return redirect('users:user_detail', self.object.pk)


class ATControllerListView(ListView):
    model = models.AirTrafficController
    # inside template `object_list` or the lowercased version of
    # the model class’s name in this case `ATController`_list is refering to the list
    # you're able to choose any name using `context_object_name`
    template_name = 'users/user_list.html'
    paginate_by = 100  # -> this will create `page_obj` for pagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ATControllerDetailView(DetailView):
    model = models.AirTrafficController
    context_object_name = 'user'
    template_name = 'users/user_detail.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             'format': '%(name)-12s %(levelname)-8s %(message)s'
#         },
#         'file': {
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
#         }
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'file',
#             'filename': '/tmp/debug.log'
#         }
#     },
#     'loggers': {
#         '': {
#             'level': 'DEBUG',
#             'handlers': ['console', 'file']
#         }
#     }
# })

# # This retrieves a Python logging instance (or creates it)
# logger = logging.getLogger(__name__)

def signup(request):
    return render(request, 'registration/signup.html')


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'users/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'users/password.html', {'form': form})
