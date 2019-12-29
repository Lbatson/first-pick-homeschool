from django.db import models
from django.forms import ModelForm


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    link = models.URLField(max_length=200)
    is_confirmed = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='curriculums')
    subjects = models.ManyToManyField(Subject, related_name='curriculums')
    grades = models.ManyToManyField(Grade, related_name='curriculums')
    levels = models.ManyToManyField(Level, related_name='curriculums')
    ages = models.ManyToManyField(Age, related_name='curriculums')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CurriculumForm(ModelForm):
    class Meta:
        model = Curriculum
        fields = ['name', 'description', 'link']
