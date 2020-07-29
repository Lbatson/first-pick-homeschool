from django.contrib.auth.models import AbstractUser
from django.db.models import (
    BooleanField,
    CharField,
    ManyToManyField,
    TextField,
    URLField,
)
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from fphs.curriculums.models import Curriculum


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(blank=True, max_length=255)
    bio = TextField(blank=True, max_length=2000)
    location = CharField(blank=True, max_length=255)
    occupation = CharField(blank=True, max_length=255)
    website = URLField(blank=True)
    facebook = URLField(blank=True)
    instagram = URLField(blank=True)
    twitter = URLField(blank=True)
    pintrest = URLField(blank=True)
    public_reviews = BooleanField(default=True)
    favorite_curriculums = ManyToManyField(
        Curriculum, blank=True, related_name="favorited_by"
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
