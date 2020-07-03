from django.urls import path

from fphs.users.views import (
    UserDetailView,
    UserRedirectView,
    UserUpdateView,
    UserProfileView,
    UserReviewsListView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("~update/", view=UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=UserDetailView.as_view(), name="detail"),
    path("<str:username>/profile", UserProfileView.as_view(), name="profile"),
    path("<str:username>/reviews", UserReviewsListView.as_view(), name="reviews"),
]
