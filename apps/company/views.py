from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from .forms import ContactUsForm
from .models import ContactUs, ManagementTeam, Timetable

# from apps.blog.models import Post


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def intro(request):
    past_3_days = datetime.now() - timedelta(days=3)
    if ContactUs.objects.filter(client_ip=get_client_ip(request),
                                created__lte=past_3_days).exists():
        form = None
    elif request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client_ip = get_client_ip(request)
            obj.save()
            return redirect('company:intro')
    else:
        form = ContactUsForm()

    timetable = Timetable.objects.active()[:10]
    if request.user.is_anonymous:
        timetable = Timetable.objects.active().filter(public=True)[:10]
    return render(request, 'company/company.html',
                  {'team': ManagementTeam.objects.first(),
                   'timetables': timetable,
                   'section': 'intro',
                   'form': form})


class TimetableDetailView(LoginRequiredMixin, DetailView):
    model = Timetable
    # template_name = "TEMPLATE_NAME"

    def get_object(self):
        object_ = get_object_or_404(Timetable, id=self.kwargs['id'])
        return object_

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "section": 'timetable_detail'
        })
        return context
