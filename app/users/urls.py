from django.urls import path

from .views import (
    UserProfileView,
    UserReviewsIndexView
)

app_name = 'users'
urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='index'),
    path('<int:pk>/reviews', UserReviewsIndexView.as_view(), name='reviews')
]
