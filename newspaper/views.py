from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, DetailView

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


class TopicDetailView(DetailView):
    model = Topic
    template_name = "newspaper/topic_detail_view.html"


class NewspaperListView(ListView):
    model = Newspaper
    paginate_by = 5


class NewspaperDetailView(DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail_view.html"


class RedactorListView(ListView):
    model = Redactor
    template_name = "newspaper/redactor_list.html"


class RedactorDetailView(DetailView):
    model = Redactor
    template_name = "newspaper/redactor_detail_view.html"
