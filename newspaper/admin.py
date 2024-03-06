from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from newspaper.models import Topic, Newspaper, Redactor


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ["topic", "title", "publish_date", ]
    list_filter = ["publish_date", "topic", ]
    search_fields = ["title", ]


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (("Years of experience", {"fields": ("years_of_experience",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "years_of_experience",)}),
    )


admin.site.register(Topic)
