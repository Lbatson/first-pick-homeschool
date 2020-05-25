from django.contrib.auth import get_user_model
from django.views import generic

from curriculums.models import Review


class UserProfileView(generic.DetailView):
    model = get_user_model()
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(user__id=self.object.id).order_by('-created')[:3]
        return context
