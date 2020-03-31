from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import (
    Curriculum,
    CurriculumForm,
    ReviewForm,
    Category,
    Subject,
    Grade,
    Level,
    Age,
    Sort,
    Review
)


class CurriculumIndexView(generic.ListView):
    model = Curriculum
    template_name = 'curriculums/index.html'
    context_object_name = 'curriculums'
    paginate_by = 20

    def get_queryset(self):
        query = Q()
        filters = self.get_filters()
        order = self.get_sort().label
        search = self.request.GET.get('search')

        if search:
            query.add(Q(name__icontains=search), Q.OR)
            query.add(Q(description__icontains=search), Q.OR)
            query.add(Q(publisher__name__icontains=search), Q.OR)

        if filters['categories']:
            query.add(Q(subjects__category__id__in=filters['categories']), Q.AND)

        if filters['subjects']:
            query.add(Q(subjects__id__in=filters['subjects']), Q.AND)

        if filters['grades']:
            query.add(Q(grades__id__in=filters['grades']), Q.AND)

        if filters['levels']:
            query.add(Q(levels__id__in=filters['levels']), Q.AND)

        if filters['ages']:
            query.add(Q(ages__id__in=filters['ages']), Q.AND)

        return Curriculum.objects.filter(query).distinct().order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = self.get_filters()
        context['sorters'] = Sort.Labels.choices
        context['sort'] = self.request.GET.get('sort')
        context['categories'] = list(Category.objects.all())
        context['subjects'] = list(Subject.objects.all())
        context['grades'] = list(Grade.objects.all())
        context['levels'] = list(Level.objects.all())
        context['ages'] = list(Age.objects.all())
        return context

    def get_filters(self):
        def get_selections(name):
            try:
                return list(map(int, self.request.GET.getlist(name)))
            except:
                return []

        return {
            'categories': get_selections('category'),
            'subjects': get_selections('subject'),
            'grades': get_selections('grade'),
            'levels': get_selections('level'),
            'ages': get_selections('age')
        }

    def get_sort(self):
        try:
            s = self.request.GET.get('sort')
            return Sort.Values(int(s)) if s.isdigit() else Sort.Values.NEWEST
        except:
            return Sort.Values.NEWEST


def detail(request, id):
    curriculum = get_object_or_404(Curriculum, pk=id, is_confirmed=True)
    categories = set(map(
        lambda s: s.category,
        curriculum.subjects.select_related('category')
    ))
    reviews = curriculum.reviews.order_by('-created')[:3]
    user_has_reviewed = curriculum.reviews.filter(user__id=request.user.id).count() > 0
    context = {
        'curriculum': curriculum,
        'categories': categories,
        'subjects': curriculum.subjects.all(),
        'grades': curriculum.grades.all(),
        'levels': curriculum.levels.all(),
        'ages': curriculum.ages.all(),
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed
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


class ReviewsIndexView(generic.ListView):
    model: Review
    template_name = 'reviews/index.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        c_id = self.kwargs.get('id')
        return Review.objects.filter(curriculum_id=c_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_has_reviewed = context['reviews'].filter(user__id=self.request.user.id).count() > 0
        context['curriculum'] = Curriculum.objects.get(id=self.kwargs.get('id'))
        context['user_has_reviewed'] = user_has_reviewed
        return context


class ReviewCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView
):
    form_class = ReviewForm
    template_name = 'reviews/create.html'
    success_message = 'Your review has been submitted'

    def get_success_url(self):
        c_id = self.kwargs.get('id')
        return reverse('curriculums:detail', kwargs={'id': c_id})

    def form_valid(self, form):
        c_id = self.kwargs.get('id')
        form.instance.curriculum = get_object_or_404(Curriculum, id=c_id)
        form.instance.user = self.request.user
        return super().form_valid(form)
