from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from newspaper.models import Topic, Redactor, Newspaper


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.topic = Topic.objects.create(name="test")
        self.redactor = Redactor.objects.create(username="testuser", first_name="test", last_name="user")
        self.newspaper = Newspaper.objects.create(title="test title", content="test content", topic=self.topic)
        self.newspaper.redactors.add(self.redactor)

    def test_topic_listed(self) -> None:
        """
        Test that topic name is listed in list_display on topic admin page
        """
        url = reverse("admin:newspaper_topic_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.topic.name)

    def test_redactor_listed(self) -> None:
        """
        Test that redactor username is listed in list_display on redactor admin page
        """
        url = reverse("admin:newspaper_redactor_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.redactor.username)

    def test_newspaper_listed(self) -> None:
        """
        Test that newspaper title is listed in list_display on newspaper admin page
        """
        url = reverse("admin:newspaper_newspaper_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.newspaper.title)
