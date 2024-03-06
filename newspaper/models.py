from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from newspaper_agency import settings


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])

    class Meta:
        ordering = ("username", )

    def __str__(self):
        return f"{self.username} | {self.first_name} {self.last_name}"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="newspapers"
    )
    redactors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="newspapers")

    class Meta:
        ordering = ("title", )

    def __str__(self):
        return f"{self.title} {self.publish_date} topic:{self.topic}"
