from django.urls import path

from fphs.users.views import (
    UserRedirectView,
    UserFavoritesView,
    UserProfileEditView,
    UserPrivacyView,
    UserProfileView,
    UserReviewsListView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("favorites/", UserFavoritesView.as_view(), name="favorites"),
    path("profile/edit/", UserProfileEditView.as_view(), name="profile-edit"),
    path("privacy/", UserPrivacyView.as_view(), name="privacy"),
    path("<str:username>/profile/", UserProfileView.as_view(), name="profile"),
    path("<str:username>/reviews/", UserReviewsListView.as_view(), name="reviews"),
]
