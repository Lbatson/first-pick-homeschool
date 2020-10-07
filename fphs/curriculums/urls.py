from django.urls import include, path

from .views import (
    CurriculumCreateView,
    CurriculumListView,
    ReviewCreateView,
    ReviewDeleteView,
    ReviewsIndexView,
    ReviewUpdateView,
    detail,
    favorite,
)

review_urls = [
    path("", ReviewsIndexView.as_view(), name="index"),
    path("create/", ReviewCreateView.as_view(), name="create"),
    path("<str:uuid>/", ReviewUpdateView.as_view(), name="update"),
    path("<str:uuid>/delete", ReviewDeleteView.as_view(), name="delete"),
]

app_name = "curriculums"

urlpatterns = [
    path("", CurriculumListView.as_view(), name="index"),
    path("create/", CurriculumCreateView.as_view(), name="create"),
    path("<slug:slug>/", detail, name="detail"),
    path("<slug:slug>/favorite/", favorite, name="favorite"),
    path(
        "<slug:slug>/reviews/", include((review_urls, "reviews"), namespace="reviews")
    ),
]
