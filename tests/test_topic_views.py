from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from newspaper.models import Topic, Newspaper

class TopicViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="test")
        self.newspaper = Newspaper.objects.create(title="test title", content="test content", topic=self.topic)
        self.newspaper.redactors.add(self.user)

    def test_topic_list_view(self):
        response = self.client.get(reverse("newspaper:topic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")

    def test_topic_detail_view(self):
        response = self.client.get(reverse("newspaper:topic-detail", args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")

    def test_topic_update_view(self):
        response = self.client.get(reverse("newspaper:topic-update", args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")

    def test_topic_delete_view(self):
        response = self.client.get(reverse("newspaper:topic-delete", args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")

    def test_topic_create_view(self):
        response = self.client.get(reverse("newspaper:topic-create"))
        self.assertEqual(response.status_code, 200)
