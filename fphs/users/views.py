from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, RedirectView, UpdateView
from fphs.curriculums.models import Review
from .forms import UserProfileForm, UserPrivacyForm

User = get_user_model()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:profile", kwargs={"username": self.request.user.username})


class UserFavoritesView(ListView):
    template_name = "users/user_favorites_list.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            self.request.user.favorite_curriculums.annotate(
                avg_rating=Coalesce(Avg("reviews__rating"), 0.0)
            )
            .all()
            .order_by("-favoritecurriculum__created")
        )


class UserProfileView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(
            user__username=self.object.username
        ).order_by("-created")[:3]
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def get_success_url(self):
        return reverse("users:profile-edit")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("Profile successfully updated")
        )
        return super().form_valid(form)


class UserPrivacyView(LoginRequiredMixin, UpdateView):
    form_class = UserPrivacyForm

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def get_success_url(self):
        return reverse("users:privacy")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _("Settings successfully updated")
        )
        return super().form_valid(form)


class UserReviewsListView(ListView):
    model = Review
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/user_reviews_list.html"
    context_object_name = "reviews"
    paginate_by = 10
    user = None

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs.get("username"))
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Review.objects.filter(user_id=self.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get(self, request, *args, **kwargs):
        # Redirect to user's profile if public reviews are disabled and accessed by a different user
        if not self.user.public_reviews and self.user != request.user:
            return redirect("users:profile", username=self.user)
        return super().get(request, *args, **kwargs)
