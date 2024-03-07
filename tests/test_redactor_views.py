from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from newspaper.models import Topic, Redactor, Newspaper

class RedactorViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="test")
        self.newspaper = Newspaper.objects.create(title="test title", content="test content", topic=self.topic)
        self.newspaper.redactors.add(self.user)

    def test_redactor_list_view(self):
        response = self.client.get(reverse("newspaper:redactor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertTemplateUsed(response, "newspaper/redactor_list.html")

    def test_redactor_detail_view(self):
        response = self.client.get(reverse("newspaper:redactor-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertTemplateUsed(response, "newspaper/redactor_detail_view.html")

    def test_redactor_create_view(self):
        response = self.client.get(reverse("newspaper:redactor-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forms/redactor_form.html")
