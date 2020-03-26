from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import (
    Curriculum,
    CurriculumForm,
    Category,
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
        query = Q()
        filters = self.get_filters()

        if filters['categories']:
            query.add(Q(subjects__category__id__in=filters['categories']), Q.OR)

        if filters['subjects']:
            query.add(Q(subjects__id__in=filters['subjects']), Q.OR)

        if filters['grades']:
            query.add(Q(grades__id__in=filters['grades']), Q.OR)

        if filters['levels']:
            query.add(Q(levels__id__in=filters['levels']), Q.OR)

        if filters['ages']:
            query.add(Q(ages__id__in=filters['ages']), Q.OR)

        return Curriculum.objects.filter(query).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = self.get_filters()
        context['categories'] = list(Category.objects.all())
        context['subjects'] = list(Subject.objects.all())
        context['grades'] = list(Grade.objects.all())
        context['levels'] = list(Level.objects.all())
        context['ages'] = list(Age.objects.all())
        return context

    def get_filters(self):
        return {
            'categories': list(map(int, self.request.GET.getlist('category'))),
            'subjects': list(map(int, self.request.GET.getlist('subject'))),
            'grades': list(map(int, self.request.GET.getlist('grade'))),
            'levels': list(map(int, self.request.GET.getlist('level'))),
            'ages': list(map(int, self.request.GET.getlist('age')))
        }


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
