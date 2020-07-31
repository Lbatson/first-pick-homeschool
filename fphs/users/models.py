from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from fphs.curriculums.models import Curriculum


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    bio = models.TextField(blank=True, max_length=2000)
    location = models.CharField(blank=True, max_length=255)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    pintrest = models.URLField(blank=True)
    public_reviews = models.BooleanField(default=True)
    favorite_curriculums = models.ManyToManyField(
        Curriculum,
        blank=True,
        related_name="favorited_by",
        through="FavoriteCurriculum",
    )

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.username})


class FavoriteCurriculum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
