from django.contrib import admin
from .models import Curriculum, Category, Subject, Grade, Level, Age

# Register your models here.
admin.site.register(Curriculum)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Level)
admin.site.register(Age)
