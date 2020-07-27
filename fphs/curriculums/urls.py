from django.urls import path

from .views import (
    CurriculumIndexView,
    detail,
    favorite,
    CurriculumCreateView,
    ReviewsIndexView,
    ReviewCreateView,
    ReviewUpdateView,
)


app_name = "curriculums"
urlpatterns = [
    path("", CurriculumIndexView.as_view(), name="index"),
    path("<int:id>/", detail, name="detail"),
    path("<int:id>/favorite", favorite, name="favorite"),
    path("create/", CurriculumCreateView.as_view(), name="create"),
    path("<int:id>/reviews", ReviewsIndexView.as_view(), name="reviews"),
    path("<int:id>/reviews/create", ReviewCreateView.as_view(), name="reviews-create"),
    path(
        "<int:id>/reviews/<int:pk>", ReviewUpdateView.as_view(), name="reviews-update"
    ),
]
