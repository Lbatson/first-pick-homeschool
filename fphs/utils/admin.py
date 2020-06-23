from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'message')
    list_display_links = ('email',)
    list_filter = ('email',)


# Register your models here.
admin.site.register(Contact, ContactAdmin)
