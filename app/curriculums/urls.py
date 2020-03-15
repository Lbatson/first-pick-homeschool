from django.urls import path

from .views import (
    CurriculumIndexView,
    detail,
    CurriculumCreateView
)


app_name = 'curriculums'
urlpatterns = [
    path('', CurriculumIndexView.as_view(), name='index'),
    path('<int:id>/', detail, name='detail'),
    path('create/', CurriculumCreateView.as_view(), name='create')
]
