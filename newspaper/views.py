from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from newspaper.models import Newspaper, Redactor, Topic


def index(request: HttpRequest) -> HttpResponse:
    num_newspapers = Newspaper.objects.count()
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()
    context = {
        "num_newspapers": num_newspapers,
        "num_redactors": num_redactors,
        "num_topics": num_topics
    }
    return render(
        request,
        template_name="newspaper/index.html",
        context=context
    )

