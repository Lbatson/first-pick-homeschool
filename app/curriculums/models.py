from django.db import models


# Create your models here.
class Curriculum(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    is_confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
