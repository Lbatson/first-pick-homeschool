from django.urls import path

from fphs.users.views import (
    UserDetailView,
    UserRedirectView,
    UserUpdateView,
    UserProfileView,
    UserReviewsIndexView
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("~update/", view=UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=UserDetailView.as_view(), name="detail"),
    path('<int:pk>/', UserProfileView.as_view(), name='index'),
    path('<int:pk>/reviews', UserReviewsIndexView.as_view(), name='reviews')
]
