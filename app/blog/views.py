from django.views import generic

from .models import Article


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class AboutView(generic.TemplateView):
    template_name = 'about.html'


class ArticleListView(generic.ListView):
    model = Article
    template_name = 'blog/index.html'


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'
