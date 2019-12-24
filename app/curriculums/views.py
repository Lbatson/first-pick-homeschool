from django.shortcuts import render

from .models import Curriculum


def index(request):
    context = {'curriculums': Curriculum.objects.all()}
    return render(request, 'curriculums/index.html', context)


def detail(request, id):
    context = {'curriculum': Curriculum.objects.get(pk=id)}
    return render(request, 'curriculums/detail.html', context)
