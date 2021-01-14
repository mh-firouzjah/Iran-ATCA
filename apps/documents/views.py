from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            TrigramSimilarity)
from django.db.models import F
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView

from apps.blog.forms import SearchForm
from apps.documents.models import DOCUMENT_TYPES, Document, DocumentCategory


def documents_archive():
    return Document.objects.active().dates('publish', 'month', order='DESC')


class DocumentListView(ListView):
    paginate_by = 10
    template_name = "documents/document_list.html"

    def get_queryset(self):
        qs = Document.objects.active()

        if 'query' in self.request.POST:
            qs = self.search(self.request)

        if 'type' in self.request.GET:
            types = self.request.GET.getlist('type')
            empty = Document.objects.none()
            for item in types:
                empty |= qs.filter(document_type=item)
            qs = empty

        if 'category' in self.request.GET:
            cat_title = self.request.GET.getlist('category')
            empty = Document.objects.none()
            for item in cat_title:
                empty |= qs.filter(categories__title_en=item)
            qs = empty

        if 'year' in self.kwargs and 'month' in self.kwargs:
            year = self.kwargs['year']
            month = self.kwargs['month']
            qs = qs.filter(publish__year=year,
                           publish__month=month)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archive = documents_archive()
        context.update({"section": "document_list",
                        "doctypes": DOCUMENT_TYPES,
                        'archive': archive,
                        'doc_cats': DocumentCategory.objects.all(),
                        'search_form': SearchForm()})
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

            search_query = SearchQuery(search_term,
                                       search_type=search_type)

            search_rank = SearchRank(F('search_vector'), search_query)

            queryset = Document.objects.active().filter(
                search_vector=search_query).annotate(
                rank=search_rank).order_by('-rank')

            if not queryset or check_for_similarities:

                similarity = sum(
                    TrigramSimilarity(x, search_term)
                    for x in ['title_fa', 'title_en',
                              'description_fa', 'description_en',
                              'content_fa', 'content_en'])

                queryset |= Document.objects.active().annotate(
                    rank=search_rank + similarity,).filter(
                        rank__gt=0.2).order_by('-rank')

            return queryset

        raise Http404('Send a search term')


class DocumentDetailView(DetailView):
    model = Document
    template_name = "documents/document_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archive = documents_archive()
        context.update({"section": "document_list",
                        "doctypes": DOCUMENT_TYPES,
                        'archive': archive,
                        'search_form': SearchForm(),
                        'doc_cats': DocumentCategory.objects.all()})
        return context
