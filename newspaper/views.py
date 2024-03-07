from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from newspaper.forms import RedactorCreationForm
from newspaper.models import Newspaper, Redactor, Topic


def index(request: HttpRequest) -> HttpResponse:
    num_newspapers = Newspaper.objects.count()
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_newspapers": num_newspapers,
        "num_redactors": num_redactors,
        "num_topics": num_topics,
        "num_visits": num_visits + 1
    }
    return render(
        request,
        template_name="newspaper/index.html",
        context=context
    )


class TopicListView(ListView):
    model = Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for topic in context['topic_list']:
            topic.latest_article = topic.newspapers.order_by('-publish_date').first()
        return context


class TopicDetailView(DetailView):
    model = Topic
    template_name = "newspaper/topic_detail_view.html"


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = "__all__"
    template_name = "forms/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = "forms/topic_confirm_delete.html"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = "__all__"
    template_name = "forms/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")


class NewspaperListView(ListView):
    model = Newspaper
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        order = self.request.GET.get("order", None)
        if order == "asc":
            queryset = queryset.order_by(F('publish_date').asc(nulls_last=True))
        elif order == "desc":
            queryset = queryset.order_by(F('publish_date').desc(nulls_last=True))
        return queryset


class NewspaperDetailView(DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail_view.html"


class NewspaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Newspaper
    fields = "__all__"
    template_name = "forms/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    fields = "__all__"
    template_name = "forms/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, DeleteView):
    model = Newspaper
    template_name = "forms/newspaper_confirm_delete.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class RedactorListView(ListView):
    model = Redactor
    template_name = "newspaper/redactor_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        order = self.request.GET.get("order", None)
        if order == "asc":
            queryset = queryset.annotate(num_newspapers=Count('newspapers')).order_by('num_newspapers')
        elif order == "desc":
            queryset = queryset.annotate(num_newspapers=Count('newspapers')).order_by('-num_newspapers')
        return queryset


class RedactorDetailView(DetailView):
    model = Redactor
    template_name = "newspaper/redactor_detail_view.html"


class RedactorCreateView(LoginRequiredMixin, CreateView):
    form_class = RedactorCreationForm
    template_name = "forms/redactor_form.html"
    success_url = reverse_lazy("newspaper:redactor-list")