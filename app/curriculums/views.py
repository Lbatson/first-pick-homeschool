from django.shortcuts import get_object_or_404, render

from .models import Curriculum, CurriculumForm


def index(request):
    context = {'curriculums': Curriculum.objects.all()}
    return render(request, 'curriculums/index.html', context)


def detail(request, id):
    curriculum = get_object_or_404(Curriculum, pk=id)
    context = {
        'curriculum': curriculum,
        'categories': curriculum.categories.all(),
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
