from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Curriculum, CurriculumForm


class IndexView(generic.ListView):
    model = Curriculum
    paginate_by = 100
    template_name = 'curriculums/index.html'
    context_object_name = 'curriculums'


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


def create(request):
    path = 'curriculums/create.html'

    if request.method == 'POST':
        form = CurriculumForm(request.POST)
        if not form.is_valid:
            context = {'error_message': form.errors}
            return render(request, path, context)
        else:
            form.save()
            context = {'form': CurriculumForm()}
            return render(request, path, context)
    else:
        context = {'form': CurriculumForm()}
        return render(request, path, context)
