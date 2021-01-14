# from hitcount.views import HitCountDetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            TrigramSimilarity)
from django.core.exceptions import PermissionDenied
from django.db.models import Count, F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from apps.users.models import AirTrafficController
from apps.users.views import user_is_atc

from .forms import CommentForm, SearchForm
from .models import Comment, Post, PostCategory, Tags


def post_archive(user=None):
    if user.is_anonymous:
        return Post.publics.dates('publish', 'month', order='DESC')
    return Post.published.dates('publish', 'month', order='DESC')


def get_post_comments(user, post):
    comments = Comment.objects.published(post)
    total_comments = comments.count()

    if user.is_anonymous:
        comments = Comment.objects.publics(post)
    return (comments, total_comments)


class PostListView(ListView):
    template_name = "components/objects_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = Post.published.all().annotate(
            total_comments=Count('comments', filter=(
                Q(comments__active=True))))

        if 'query' in self.request.POST:
            qs = self.search(self.request)

        if 'tag' in self.request.GET:
            tag = get_object_or_404(Tags, name=self.request.GET['tag'])
            qs = qs.filter(tags__in=[tag.id])

        if 'category' in self.request.GET:
            cat = get_object_or_404(PostCategory, slug=self.request.GET['category'])
            qs = qs.filter(categories__in=[cat])

        if self.request.user.is_anonymous:
            qs = Post.publics.all().annotate(
                total_comments=Count('comments', filter=(
                    Q(comments__active=True))))

        if 'year' in self.kwargs and 'month' in self.kwargs:
            qs = qs.filter(
                publish__year=self.kwargs['year'],
                publish__month=self.kwargs['month']).annotate(
                total_comments=Count('comments', filter=(
                    Q(comments__active=True))))

        if 'user_name' in self.kwargs:
            qs = qs.filter(author=self.kwargs['username'])

        if get_language() == 'en':
            qs = qs.filter(international=True)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = SearchForm()
        context.update({
            # 'popular_objects': popular_posts(user=self.request.user),
            'latest_objects': Post.objects.all()[:5],
            'archive': post_archive(user=self.request.user),
            'section': 'post_list',
            'search_form': search_form})
        return context

    def post(self, request, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context.update({
            'object_list': self.object_list,
            'search_form': SearchForm(request.POST)
        })
        return render(request, self.template_name, context)

    def search(self, request):
        form = SearchForm(request.POST, None)
        if form.is_valid():
            search_term = form.cleaned_data['query']
            check_for_similarities = form.cleaned_data['check_for_similarities']
            search_type = 'plain' if not form.cleaned_data.get(
                'consider_one_phrase') else 'phrase'

            search_query = SearchQuery(
                search_term, search_type=search_type)

            search_rank = SearchRank(F('search_vector'), search_query)

            queryset = Post.published.filter(search_vector=search_query).annotate(
                total_comments=Count('comments', filter=(Q(comments__active=True))),
                rank=search_rank).order_by('-rank')

            if not queryset or check_for_similarities:

                similarity = sum(
                    TrigramSimilarity(x, search_term)
                    for x in ['title_fa', 'title_en', 'body_fa', 'body_en'])

                queryset |= Post.published.annotate(
                    total_comments=Count('comments', filter=(Q(comments__active=True))),
                    rank=search_rank + similarity).filter(
                        rank__gt=0.2).order_by('-rank')

            return queryset
        raise Http404('Send a search term')


class PostDetailView(DetailView):
    model = Post
    # template_name = "post_detail.html"
    context_object_name = 'post'
    count_hit = True

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, slug=kwargs['slug'],
                                      status='published',
                                      publish__year=kwargs['year'],
                                      publish__month=kwargs['month'],
                                      publish__day=kwargs['day'])

        if self.request.user.is_anonymous and not self.post.public:
            raise PermissionDenied(
                _("You don't have permission to read a private page."))

        if get_language() == 'en' \
                and not self.post.international:
            raise Http404(_("Requested page is not in English!"))

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):

        comments, total_comments = get_post_comments(self.request.user, self.object)
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        posts = Post.published.all()
        if self.request.user.is_anonymous:
            posts = Post.publics.all()
        similar_posts = posts.filter(tags__in=post_tags_ids
                                     ).exclude(id=self.object.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')
                                               ).order_by('-same_tags', '-publish')[:5]
        context = super().get_context_data(**kwargs)
        context.update({
            # 'popular_objects': popular_posts(self.object, self.request.user),
            'latest_objects': Post.objects.all()[:5],
            'similar_objects': similar_posts,
            'archive': post_archive(user=self.request.user),
            'comments': comments,
            'total_comments': total_comments,
            'author': self.object.author,
            'post_tags': self.object.tags.all(),
            'post_images': self.object.images.all(),
            'section': 'post_detail',
            'search_form': SearchForm()
        })
        return context


@login_required(login_url='users:login')
@user_passes_test(user_is_atc)
def add_comment(request, post_id, comment_id=None):
    post = get_object_or_404(Post, id=post_id)
    user = AirTrafficController.objects.get(user=request.user)
    comment = None
    if comment_id:
        comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST, None)

    context = {
        'form': form,
        'post_id': post_id,
        'comment_id': comment_id,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        instance.post = post
        instance.replied = comment
        instance.save()
        return redirect(post)
    return render(request, 'blog/comment_form.html', context)
