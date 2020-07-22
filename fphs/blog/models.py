from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

from wagtailmetadata.models import MetadataPageMixin


class BlogIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_posts(self):
        return self.get_children().live().public().order_by("-first_published_at")

    def paginate(self, request):
        page = request.GET.get("page")
        paginator = Paginator(self.get_posts(), 10)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request, **kwargs):
        context = super().get_context(request)
        context["posts"] = self.paginate(request)
        return context


class BlogPost(MetadataPageMixin, Page):
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
