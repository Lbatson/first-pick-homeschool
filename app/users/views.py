from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views import generic

from curriculums.models import Review


class UserProfileView(generic.DetailView):
    model = get_user_model()
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(user__id=self.object.id).order_by('-created')[:3]
        return context


class UserReviewsIndexView(generic.ListView):
    model: Review
    template_name = 'users/list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        u_id = self.kwargs.get('pk')
        return Review.objects.filter(user_id=u_id)

    def get_context_data(self, **kwargs):
        u_id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(get_user_model(), id=u_id)
        return context
