from django.urls import include, path

from .views import (
    CurriculumListView,
    detail,
    favorite,
    CurriculumCreateView,
    ReviewsIndexView,
    ReviewCreateView,
    ReviewUpdateView,
)

review_urls = [
    path("", ReviewsIndexView.as_view(), name="index"),
    path("create/", ReviewCreateView.as_view(), name="create"),
    path("<str:uuid>/", ReviewUpdateView.as_view(), name="update"),
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
