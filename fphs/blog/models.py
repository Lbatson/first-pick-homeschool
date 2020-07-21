from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index


class BlogIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)
        context["posts"] = self.get_children().live().order_by("-first_published_at")
        return context


class BlogPost(Page):
    description = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    date = models.DateField("Post date")

    search_fields = Page.search_fields + [
        index.SearchField("description"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("body", classname="full"),
        FieldPanel("date"),
    ]
