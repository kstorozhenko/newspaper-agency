from django.test import TestCase
from newspaper.forms import RedactorCreationForm, NewspaperForm, NewspaperSearchForm
from newspaper.models import Redactor, Topic, Newspaper


class FormTests(TestCase):
    def setUp(self):
        self.user = Redactor.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="test",
            last_name="user",
            email="testuser@example.com",
            years_of_experience=5
        )
        self.topic = Topic.objects.create(name="test")
        self.newspaper = Newspaper.objects.create(title="test title", content="test content", topic=self.topic)
        self.newspaper.redactors.add(self.user)

    def test_redactor_creation_form(self):
        form = RedactorCreationForm(
            data={
                "username": "testuser2",
                "password1": "testpassword2",
                "password2": "testpassword2",
                "first_name": "test2",
                "last_name": "user2",
                "email": "testuser2@example.com",
                "years_of_experience": 6
            }
        )
        self.assertTrue(form.is_valid())

    def test_newspaper_form(self):
        form = NewspaperForm(
            data={
                "title": "test title 2",
                "content": "test content 2",
                "topic": self.topic.id,
                "authors": [self.user.id]
            }
        )
        self.assertTrue(form.is_valid())

    def test_newspaper_search_form(self):
        form = NewspaperSearchForm(data={"title": "test title"})
        self.assertTrue(form.is_valid())
