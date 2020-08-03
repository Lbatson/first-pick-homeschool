from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import (
    Curriculum,
    Category,
    Subject,
    Grade,
    Age,
    ReligiousPreference,
    Publisher,
    Review,
)


class CategoryAdmin(ModelAdmin):
    model = Category


class SubjectAdmin(ModelAdmin):
    model = Subject


class GradeAdmin(ModelAdmin):
    model = Grade


class AgeAdmin(ModelAdmin):
    model = Age


class ReligiousPreferenceAdmin(ModelAdmin):
    model = ReligiousPreference


class PublisherAdmin(ModelAdmin):
    model = Publisher
    list_display = (
        "name",
        "link",
    )
    search_fields = ("name",)


class CurriculumAdmin(ModelAdmin):
    model = Curriculum
    list_display = (
        "name",
        "is_confirmed",
        "created_by",
    )
    list_filter = (
        "is_confirmed",
        "subjects__category",
        "subjects",
        "grades",
        "ages",
    )
    search_fields = (
        "name",
        "created_by__username",
    )


class ReviewAdmin(ModelAdmin):
    model = Review
    list_display = (
        "content",
        "rating",
        "verified",
        "user",
    )
    list_filter = ("verified",)
    search_fields = ("user__username",)


class HomeschoolGroup(ModelAdminGroup):
    menu_label = "Homeschool"
    items = (
        CategoryAdmin,
        SubjectAdmin,
        GradeAdmin,
        AgeAdmin,
        ReligiousPreferenceAdmin,
        PublisherAdmin,
        CurriculumAdmin,
        ReviewAdmin,
    )


modeladmin_register(HomeschoolGroup)
