from django.urls import path

from .views import (
    IndexView,
    AboutView,
    ArticleListView,
    ArticleDetailView
)


app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('blog/', ArticleListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', ArticleDetailView.as_view(), name='detail')
]
