from django.urls import path

from fphs.users.views import (
    UserRedirectView,
    UserProfileView,
    UserProfileEditView,
    UserReviewsListView,
)

app_name = "users"
urlpatterns = [
    path("profile/edit/", UserProfileEditView.as_view(), name="edit-profile"),
    path("<str:username>/profile/", UserProfileView.as_view(), name="profile"),
    path("<str:username>/reviews/", UserReviewsListView.as_view(), name="reviews"),
]
