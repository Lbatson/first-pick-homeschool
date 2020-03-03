from django.urls import path

from . import views

app_name = 'curriculums'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('create/', views.create, name='create')
]
