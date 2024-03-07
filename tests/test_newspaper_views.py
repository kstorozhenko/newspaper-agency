from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from newspaper.models import Topic, Redactor, Newspaper


class NewspaperViewsTest(TestCase):
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

    def test_newspaper_list_view(self):
        response = self.client.get(reverse("newspaper:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test title")

    def test_newspaper_detail_view(self):
        response = self.client.get(reverse("newspaper:newspaper-detail", args=[self.newspaper.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test title")

    def test_newspaper_update_view(self):
        response = self.client.get(reverse("newspaper:newspaper-update", args=[self.newspaper.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test title")

    def test_newspaper_delete_view(self):
        response = self.client.get(reverse("newspaper:newspaper-delete", args=[self.newspaper.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test title")

    def test_newspaper_create_view(self):
        response = self.client.get(reverse("newspaper:newspaper-create"))
        self.assertEqual(response.status_code, 200)
