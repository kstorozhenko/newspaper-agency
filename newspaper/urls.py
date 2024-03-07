from django.urls import path

from newspaper.views import index, TopicListView, NewspaperListView, NewspaperDetailView, RedactorListView, \
    RedactorDetailView, TopicDetailView, TopicCreateView, NewspaperCreateView

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topics/<int:pk>", TopicDetailView.as_view(), name="topic-detail"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>", RedactorDetailView.as_view(), name="redactor-detail")


]

app_name = "newspaper"
