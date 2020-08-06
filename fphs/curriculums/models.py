from django.conf import settings
from django.db import models
from django.forms import ModelForm, TextInput, Textarea, Select
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subjects",
    )

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class ReligiousPreference(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Sort:
    class Labels(models.IntegerChoices):
        NEWEST = (
            1,
            _("Newest"),
        )
        OLDEST = (
            2,
            _("Oldest"),
        )
        HIGHEST_RATING = (
            3,
            _("Highest Rating"),
        )
        LOWEST_RATING = (
            4,
            _("Lowest Rating"),
        )
        NAME = (
            5,
            _("A-Z"),
        )
        NAME_REVERSED = 6, _("Z-A")

    class Values(models.IntegerChoices):
        NEWEST = (
            1,
            "-created",
        )
        OLDEST = (
            2,
            "created",
        )
        HIGHEST_RATING = (
            3,
            "-avg_rating",
        )
        LOWEST_RATING = (
            4,
            "avg_rating",
        )
        NAME = (
            5,
            "name",
        )
        NAME_REVERSED = 6, "-name"


class Curriculum(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    slug = models.SlugField(max_length=200, unique=True)
    link = models.URLField(max_length=200)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL
    )
    is_confirmed = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject, related_name="curriculums")
    grades = models.ManyToManyField(Grade, related_name="curriculums")
    ages = models.ManyToManyField(Age, related_name="curriculums")
    religious_preference = models.ForeignKey(
        ReligiousPreference,
        null=True,
        on_delete=models.SET_NULL,
        related_name="curriculums",
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="curriculums"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="curriculums",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("curriculums:detail", kwargs={"slug": self.slug})


class CurriculumForm(ModelForm):
    class Meta:
        model = Curriculum
        fields = ["name", "description", "link", "publisher"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "link": TextInput(attrs={"class": "form-control"}),
            "publisher": Select(attrs={"class": "form-control"}),
        }


class Review(models.Model):
    RATING_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))

    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name="reviews"
    )
    content = models.TextField(max_length=5000, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    verified = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated"]

    def __str__(self):
        return f"{self.curriculum} - {self.rating} - {self.user.email}"


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating"]
        labels = {
            "content": _("Review"),
        }
        widgets = {
            "content": Textarea(attrs={"class": "form-control"}),
            "rating": Select(attrs={"class": "form-control"}),
        }
