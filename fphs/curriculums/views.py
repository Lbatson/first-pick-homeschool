from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Q
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_GET

from fphs.users.models import User
from fphs.utils.models import Metadata

from .models import (
    Age,
    Category,
    Curriculum,
    CurriculumForm,
    Grade,
    ReligiousPreference,
    Review,
    ReviewForm,
    Sort,
    Subject,
)


class CurriculumListView(generic.ListView):
    model = Curriculum
    template_name = "curriculums/index.html"
    context_object_name = "curriculums"
    paginate_by = 20

    def get_queryset(self):
        query = Q()
        filters = self.get_filters()
        order = self.get_sort().label
        search = self.request.GET.get("q")

        if search:
            query.add(Q(name__icontains=search), Q.OR)
            query.add(Q(description__icontains=search), Q.OR)
            query.add(Q(publisher__name__icontains=search), Q.OR)

        if filters["categories"]:
            query.add(Q(subjects__category__id__in=filters["categories"]), Q.AND)

        if filters["subjects"]:
            query.add(Q(subjects__id__in=filters["subjects"]), Q.AND)

        if filters["grades"]:
            query.add(Q(grades__id__in=filters["grades"]), Q.AND)

        if filters["ages"]:
            query.add(Q(ages__id__in=filters["ages"]), Q.AND)

        if filters["preference"]:
            query.add(Q(religious_preference__id__in=filters["preference"]), Q.AND)

        return (
            Curriculum.objects.annotate(
                avg_rating=Coalesce(Avg("reviews__rating"), 0.0)
            )
            .filter(is_confirmed=True)
            .filter(query)
            .distinct()
            .order_by(order)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("search")
        context["filters"] = self.get_filters()
        context["sorters"] = Sort.Labels.choices
        context["sort"] = self.request.GET.get("sort")
        context["categories"] = list(Category.objects.all())
        context["subjects"] = list(Subject.objects.all())
        context["grades"] = list(Grade.objects.all())
        context["ages"] = list(Age.objects.all())
        context["preference"] = list(ReligiousPreference.objects.all())
        context["metadata"] = Metadata(
            self.request, "Curriculums", "List of curriculums"
        )
        return context

    def get_filters(self):
        def get_selections(name):
            try:
                return list(map(int, self.request.GET.getlist(name)))
            except Exception:
                return []

        return {
            "categories": get_selections("category"),
            "subjects": get_selections("subject"),
            "grades": get_selections("grade"),
            "ages": get_selections("age"),
            "preference": get_selections("preference"),
        }

    def get_sort(self):
        try:
            s = self.request.GET.get("sort")
            return Sort.Values(int(s)) if s.isdigit() else Sort.Values.NEWEST
        except Exception:
            return Sort.Values.NEWEST


@require_GET
def detail(request, slug):
    curriculum = get_object_or_404(Curriculum, slug=slug, is_confirmed=True)
    categories = set(
        map(lambda s: s.category, curriculum.subjects.select_related("category"))
    )
    reviews = curriculum.reviews.order_by("-created")[:3]

    def get_values(items):
        return items[0], items[-1] if len(items) > 1 else None

    context = {
        "curriculum": curriculum,
        "categories": categories,
        "subjects": curriculum.subjects.all(),
        "grades": get_values(list(curriculum.grades.all())),
        "ages": get_values(list(curriculum.ages.all())),
        "reviews": reviews,
        "avg_rating": reviews.aggregate(avg_rating=Coalesce(Avg("rating"), 0.0))[
            "avg_rating"
        ],
    }
    return render(request, "curriculums/detail.html", context)


@login_required
def favorite(request, slug):
    curriculum = get_object_or_404(Curriculum, slug=slug, is_confirmed=True)
    # Redirect to detail page after login
    if request.method == "GET":
        return HttpResponseRedirect(
            reverse("curriculums:detail", kwargs={"slug": curriculum.slug})
        )

    # Save favorite and go back to previous page
    user: User = request.user
    if curriculum in user.favorite_curriculums.all():
        user.favorite_curriculums.remove(curriculum)
    else:
        user.favorite_curriculums.add(curriculum)
    user.save()
    return HttpResponseRedirect(request.POST.get("next", "/"))


class CurriculumCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = CurriculumForm
    template_name = "curriculums/create.html"
    success_url = "/curriculums/create/"
    success_message = "Your request to add a curriculum was submitted"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ReviewsIndexView(generic.ListView):
    model: Review
    template_name = "reviews/index.html"
    context_object_name = "reviews"
    paginate_by = 20

    def get_queryset(self):
        curriculum = get_object_or_404(
            Curriculum, slug=self.kwargs.get("slug"), is_confirmed=True
        )
        return Review.objects.filter(curriculum_id=curriculum.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["curriculum"] = get_object_or_404(
            Curriculum, slug=self.kwargs.get("slug")
        )
        return context


class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = ReviewForm
    template_name = "reviews/create.html"
    success_message = "Your review has been submitted"

    def get_success_url(self):
        return reverse("curriculums:detail", kwargs={"slug": self.kwargs.get("slug")})

    def form_valid(self, form):
        form.instance.curriculum = get_object_or_404(
            Curriculum, slug=self.kwargs.get("slug")
        )
        form.instance.user = self.request.user
        return super().form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        slug = self.kwargs.get("slug")
        curriculum = get_object_or_404(Curriculum, slug=slug)
        context["curriculum"] = curriculum
        review = (
            curriculum.reviews.filter(user__id=self.request.user.id).first() or None
        )
        # Redirect user to update review if one exists
        if review:
            return redirect(
                "curriculums:reviews:update", slug=curriculum.slug, uuid=review.uuid
            )
        return super().render_to_response(context, **response_kwargs)


class ReviewUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = ReviewForm
    template_name = "reviews/create.html"
    success_message = "Your review has been updated"

    def get_success_url(self):
        return reverse("curriculums:detail", kwargs={"slug": self.kwargs.get("slug")})

    def get_object(self, queryset=None):
        return get_object_or_404(Review, uuid=self.kwargs.get("uuid"))

    def render_to_response(self, context, **response_kwargs):
        # Prevent editing a review by another user
        if self.request.user != self.object.user:
            return redirect("curriculums:detail", slug=self.kwargs.get("slug"))
        context["curriculum"] = get_object_or_404(
            Curriculum, slug=self.kwargs.get("slug")
        )
        return super().render_to_response(context, **response_kwargs)


class ReviewDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    context_object_name = "review"
    template_name = "reviews/delete.html"

    def get_success_url(self):
        return reverse("curriculums:detail", kwargs={"slug": self.kwargs.get("slug")})

    def get_object(self, queryset=None):
        return get_object_or_404(Review, uuid=self.kwargs.get("uuid"))

    def get(self, request, *args, **kwargs):
        # Preview viewing delete page for review by another user
        if request.user != self.get_object().user:
            return redirect("curriculums:detail", slug=self.kwargs.get("slug"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Prevent deleting a review by another user
        if request.user != self.get_object().user:
            return redirect("curriculums:detail", slug=self.kwargs.get("slug"))
        return super().post(request, *args, **kwargs)
