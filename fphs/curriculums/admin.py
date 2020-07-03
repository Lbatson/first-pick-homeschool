from django.contrib import admin

from .models import (
    Curriculum,
    Category,
    Subject,
    Grade,
    Age,
    ReligiousPreference,
    Publisher,
)


class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "link", "is_confirmed")
    list_display_links = ("name",)
    list_filter = ("is_confirmed", "subjects__category", "subjects", "grades", "ages")


class PublisherAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link")
    list_display_links = ("name",)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_display_links = ("name",)


# Register your models here.
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Category)
admin.site.register(Grade)
admin.site.register(Age)
admin.site.register(ReligiousPreference)
