from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'message', 'replied')
    list_display_links = ('email',)
    list_filter = ('replied',)


# Register your models here.
admin.site.register(Contact, ContactAdmin)
