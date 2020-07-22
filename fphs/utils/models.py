from django.db import models

from wagtailmetadata.models import MetadataMixin


class Metadata(MetadataMixin):
    def __init__(self, request, title, description, image=None):
        self.request = request
        self.title = title
        self.description = description
        self.image = image

    def get_meta_url(self):
        return self.request.build_absolute_uri()

    def get_meta_title(self):
        return self.title

    def get_meta_description(self):
        return self.description

    def get_meta_image(self):
        return self.image


class Contact(models.Model):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
    message = models.TextField(max_length=2000)
    replied = models.BooleanField(default=False)
