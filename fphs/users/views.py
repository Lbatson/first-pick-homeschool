from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, RedirectView, UpdateView

from fphs.curriculums.models import Review

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Profile successfully updated")
        )
        return super().form_valid(form)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserProfileView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(
            user__username=self.object.username
        ).order_by("-created")[:3]
        return context


class UserReviewsListView(ListView):
    model = Review
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/list.html"
    context_object_name = "reviews"
    user = None

    def get_queryset(self):
        username = self.kwargs.get("username")
        self.user = get_object_or_404(User, username=username)
        return Review.objects.filter(user_id=self.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context
