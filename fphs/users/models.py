from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ManyToManyField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from fphs.curriculums.models import Curriculum


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    favorite_curriculums = ManyToManyField(
        Curriculum, blank=True, related_name="favorited_by"
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
