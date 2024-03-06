from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from newspaper.models import Topic, Newspaper, Redactor

admin.site.register(Topic)
admin.site.register(Newspaper)
admin.site.register(Redactor, UserAdmin)
