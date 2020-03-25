from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import (
    Curriculum,
    CurriculumForm,
    Subject,
    Grade,
    Level,
    Age
)


class CurriculumIndexView(generic.ListView):
    model = Curriculum
    template_name = 'curriculums/index.html'
    context_object_name = 'curriculums'

    def get_queryset(self):
        return Curriculum.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['grades'] = Grade.objects.all()
        context['levels'] = Level.objects.all()
        context['ages'] = Age.objects.all()
        return context


def detail(request, id):
    curriculum = get_object_or_404(Curriculum, pk=id, is_confirmed=True)
    categories = set(map(
        lambda s: s.category,
        curriculum.subjects.select_related('category')
    ))
    context = {
        'curriculum': curriculum,
        'categories': categories,
        'subjects': curriculum.subjects.all(),
        'grades': curriculum.grades.all(),
        'levels': curriculum.levels.all(),
        'ages': curriculum.ages.all()
    }
    return render(request, 'curriculums/detail.html', context)


class CurriculumCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView
):
    form_class = CurriculumForm
    template_name = 'curriculums/create.html'
    success_url = '/curriculums/create/'
    success_message = 'Your request to add a curriculum was submitted'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
