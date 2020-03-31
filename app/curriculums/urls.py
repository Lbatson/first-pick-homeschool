from django.urls import path

from .views import (
    CurriculumIndexView,
    detail,
    CurriculumCreateView,
    ReviewsIndexView,
    ReviewCreateView
)


app_name = 'curriculums'
urlpatterns = [
    path('', CurriculumIndexView.as_view(), name='index'),
    path('<int:id>/', detail, name='detail'),
    path('create/', CurriculumCreateView.as_view(), name='create'),
    path('<int:id>/reviews', ReviewsIndexView.as_view(), name='reviews'),
    path('<int:id>/reviews/create', ReviewCreateView.as_view(), name='reviews-create')
]
