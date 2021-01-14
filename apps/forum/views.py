from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import \
    TrigramSimilarity  # ,TrigramDistance
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Max, Q
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from apps.blog.forms import SearchForm
from apps.users.models import AirTrafficController
from apps.users.views import user_is_atc

from .forms import ChatForm
from .models import Chat, Forum

# from hitcount.views import HitCountDetailView


def forum_archive():
    return Forum.objects.active().dates('publish', 'month', order='DESC')


class ForumListView(LoginRequiredMixin, ListView):
    template_name = "components/objects_list.html"
    # ordering = ('publish',)
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not user_is_atc(self.request.user):
            raise PermissionDenied(_(
                "You have to be a registered ATCo in Iran-ATCA."))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Forum.objects.active().annotate(
            total_comments=Count('chats', filter=(
                Q(chats__active=True))))

        if 'forum_name' in self.kwargs:
            qs = qs.filter(name__icontains=self.kwargs['forum_name'])

        if 'year' in self.kwargs and 'month' in self.kwargs:
            qs = qs.filter(
                publish__year=self.kwargs['year'],
                publish__month=self.kwargs['month']).annotate(
                total_comments=Count('chats', filter=(Q(chats__active=True))))

        if 'query' in self.request.POST:
            qs = self.search(self.request)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_forums = Forum.objects.active()[:5]
        last_active_forums = Forum.objects.annotate(latest_active=(
            Coalesce(Max('chats__created'), 'publish'))).order_by('latest_active')[:5]
        context.update({
            # 'popular_objects': popular_posts(user=self.request.user),
            'archive': forum_archive(),
            'section': 'forum_list',
            'latest_objects': latest_forums,
            'last_active_objects': last_active_forums,
            'search_form': SearchForm()
        })
        return context

    def post(self, request, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        context.update({
            'object_list': self.object_list,
            'search_form': SearchForm(request.POST)
        })
        return render(request, self.template_name, context)

    def search(self, request):
        form = SearchForm(request.POST, None)
        if form.is_valid():
            search_term = form.cleaned_data['query']

            similarity = sum(TrigramSimilarity(x, search_term)
                             for x in ['name', 'description', 'chats__content'])
            # distance = min(TrigramDistance(x, search_term)
            #                for x in ['name', 'description', 'chats__content'])

            queryset = Forum.objects.active().annotate(
                total_comments=Count('chats', filter=(Q(chats__active=True))),
                rank=similarity,).filter(rank__gt=0.2).order_by('-rank')

            return queryset
        raise Http404('Send a search term')


class ForumDetailView(LoginRequiredMixin, DetailView):
    model = Forum
    # context_object_name = 'forum'
    count_hit = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('users:login')

        if not user_is_atc(self.request.user):
            raise PermissionDenied(_(
                "You have to be a registered ATCo in Iran-ATCA."))

        forum = Forum.objects.get(pk=kwargs['pk'])

        if AirTrafficController.objects.filter(user=request.user).exists():
            if request.user.atc_info not in forum.members.all():
                raise PermissionDenied(
                    _("You are not a member of this forum."))
        else:
            raise PermissionDenied(
                _("You are not a member of this forum."))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        forum_chats = self.object.chats.filter(active=True)
        latest_forums = Forum.objects.all()[:5]
        last_active_forums = Forum.objects.annotate(latest_active=(
            Coalesce(Max('chats__created'), 'publish'))).order_by('latest_active')[:5]
        context = super().get_context_data(**kwargs)
        form = ChatForm()
        context.update({'forum_chats': forum_chats, 'form': form,
                        'g_user': AirTrafficController.objects.get(
                            user=self.request.user),
                        'broadcast': False,
                        'archive': forum_archive(),
                        'latest_objects': latest_forums,
                        'last_active_objects': last_active_forums,
                        'search_form': SearchForm()})
        return context


@login_required
@user_passes_test(user_is_atc)
def add_chat(request, chat_id=None):
    return render(request, 'forum/chat-form.html',
                  {'form': ChatForm(),
                   'chat_id': chat_id,
                   'edit': False})


@login_required
@user_passes_test(user_is_atc)
def delete_chat(request, chat_id):
    return render(request, 'forum/chat-delete-confirm.html',
                  {'chat_id': chat_id})


@login_required
@user_passes_test(user_is_atc)
def edit_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return render(request, 'forum/chat-form.html',
                  {'form': ChatForm(instance=chat),
                   'chat_id': chat_id,
                   'edit': True})


@login_required
@user_passes_test(user_is_atc)
def join_forum_and_redirect(request, pk, token):
    forum = get_object_or_404(Forum, pk=pk)
    user = request.user.atc_info
    if token in forum.invite_link:
        forum.members.add(user)
        return redirect('forum:room', pk)
    raise Http404("Incorrect link")
