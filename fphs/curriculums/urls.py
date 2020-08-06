from django.urls import path

from .views import (
    CurriculumListView,
    detail,
    favorite,
    CurriculumCreateView,
    ReviewsIndexView,
    ReviewCreateView,
    ReviewUpdateView,
)


app_name = "curriculums"
urlpatterns = [
    path("", CurriculumListView.as_view(), name="index"),
    path("<slug:slug>/", detail, name="detail"),
    path("<slug:slug>/favorite/", favorite, name="favorite"),
    path("create/", CurriculumCreateView.as_view(), name="create"),
    path("<slug:slug>/reviews/", ReviewsIndexView.as_view(), name="reviews"),
    path(
        "<slug:slug>/reviews/create/", ReviewCreateView.as_view(), name="reviews-create"
    ),
    path(
        "<slug:slug>/reviews/<int:pk>/",
        ReviewUpdateView.as_view(),
        name="reviews-update",
    ),
]
