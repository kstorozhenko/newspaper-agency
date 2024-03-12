from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from newspaper.forms import (RedactorCreationForm,
                             NewspaperForm,
                             NewspaperSearchForm)
from newspaper.models import (Newspaper,
                              Redactor,
                              Topic)


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
            topic.latest_article = (topic.newspapers.order_by('-publish_date').first())

        return context


class TopicDetailView(DetailView):
    model = Topic
    template_name = "newspaper/topic_detail_view.html"


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = "__all__"
    template_name = "forms/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "newspaper/dont_have_permission.html")

        return super().dispatch(request, *args, **kwargs)


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = "forms/topic_confirm_delete.html"
    success_url = reverse_lazy("newspaper:topic-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "newspaper/dont_have_permission.html")

        return super().dispatch(request, *args, **kwargs)


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = "__all__"
    template_name = "forms/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "newspaper/dont_have_permission.html")

        return super().dispatch(request, *args, **kwargs)


class NewspaperListView(ListView):
    model = Newspaper
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.select_related("topic")
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])

        return queryset


class NewspaperDetailView(DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail_view.html"


class NewspaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "forms/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "newspaper/dont_have_permission.html")

        return super().dispatch(request, *args, **kwargs)


class NewspaperCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "forms/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "newspaper/dont_have_permission.html")

        return super().dispatch(request, *args, **kwargs)


class NewspaperDeleteView(LoginRequiredMixin, DeleteView):
    model = Newspaper
    template_name = "forms/newspaper_confirm_delete.html"
    success_url = reverse_lazy("newspaper:newspaper-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "newspaper/dont_have_permission.html")

        return super().dispatch(request, *args, **kwargs)


class RedactorListView(ListView):
    model = Redactor
    template_name = "newspaper/redactor_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        order = self.request.GET.get("order", "asc")
        if order == "desc":
            queryset = (queryset.
                        annotate(num_newspapers=Count('newspapers')).
                        order_by('-num_newspapers'))
        else:
            queryset = (queryset.
                        annotate(num_newspapers=Count('newspapers')).
                        order_by('num_newspapers'))

        return queryset


class RedactorDetailView(DetailView):
    model = Redactor
    template_name = "newspaper/redactor_detail_view.html"


class RedactorCreateView(LoginRequiredMixin, CreateView):
    form_class = RedactorCreationForm
    template_name = "forms/redactor_form.html"
    success_url = reverse_lazy("newspaper:redactor-list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, "newspaper/dont_have_permission.html")

        return super().dispatch(request, *args, **kwargs)
