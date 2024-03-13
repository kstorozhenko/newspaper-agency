from django.test import TestCase
from newspaper.models import Topic, Redactor, Newspaper

class TestModels(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), "test")

    def test_redactor_str(self):
        redactor = Redactor.objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.assertEqual(str(redactor), "test_username | test_first_name test_last_name")

    def test_newspaper_str(self):
        topic = Topic.objects.create(name="test")
        redactor = Redactor.objects.create(username="test_username")
        newspaper = Newspaper.objects.create(
            title="test_title",
            content="test_content",
            topic=topic
        )
        newspaper.redactors.add(redactor)
        self.assertEqual(str(newspaper), f"test_title {newspaper.publish_date} topic:test")
