from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


def bad_request(request, exception='') -> 400:
    return render(request, 'errors/400.html', {'exception': exception})


def permission_denied(request, exception='') -> 403:
    return render(request, 'errors/403.html', {'exception': exception})


def page_not_found(request, exception='') -> 404:
    return render(request, 'errors/404.html', {'exception': exception})


def server_error(request) -> 500:
    return render(request, 'errors/500.html',)


def csrf_failure(request, reason="") -> 'csrf_403':
    '''
    Reason is a short message (intended for developers or logging, not for end users)
    '''
    return render(request, 'errors/403_csrf.html', {'reason': reason})


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'authentication/login.html'
    success_message = _('Welcome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.username
        return context


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
