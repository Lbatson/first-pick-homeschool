from django.contrib import admin
from .models import Curriculum, Category, Subject, Grade, Level, Age


class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'is_confirmed')


# Register your models here.
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Level)
admin.site.register(Age)
