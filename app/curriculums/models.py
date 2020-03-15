from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

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
        related_name='subjects'
    )

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


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Curriculum(models.Model):

    class Format(models.TextChoices):
        RESOURCE = 'R', _('Resource')
        TEXTBOOK = 'T', _('Textbook')
        WORKBOOK = 'W', _('Workbook')

    class Consumable(models.TextChoices):
        YES = 'Y', _('Yes')
        NO = 'N', _('No')
        MIXED = 'M', _('Mixed')

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    link = models.URLField(max_length=200)
    is_confirmed = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject, related_name='curriculums')
    grades = models.ManyToManyField(Grade, related_name='curriculums')
    levels = models.ManyToManyField(Level, related_name='curriculums')
    ages = models.ManyToManyField(Age, related_name='curriculums')
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='curriculums'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    subscription = models.BooleanField(default=False)
    format = models.CharField(
        max_length=1,
        null=True,
        choices=Format.choices
    )
    consumable = models.CharField(
        max_length=1,
        null=True,
        choices=Consumable.choices
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='curriculums'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CurriculumForm(ModelForm):
    class Meta:
        model = Curriculum
        fields = ['name', 'description', 'link', 'publisher']
