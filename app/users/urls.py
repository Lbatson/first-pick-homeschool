from django.urls import path

from .views import UserProfileView


app_name = 'users'
urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='index')
]
