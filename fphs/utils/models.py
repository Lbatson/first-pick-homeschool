from django.db import models


class Contact(models.Model):
    email = models.EmailField(
        blank=False,
        max_length=254,
        verbose_name="email address"
    )
    message = models.TextField(max_length=2000)
    replied = models.BooleanField(default=False)
