from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.decorators.http import require_GET
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .forms import ContactForm
from .models import Contact


@require_GET
def robots_txt(request):
    isProd = request.get_host().split('.')[0] == "firstpickhomeschool"
    lines = [
        "User-Agent: *",
        f"Disallow: {'/admin' if isProd else '/'}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


class ContactView(FormView):
    form_class = ContactForm
    template_name = "pages/contact.html"

    def form_invalid(self, form):
        if form.errors.as_data()["captcha"]:
            messages.error(self.request, _(
                "Sorry, but we're unable to process your request at this time."
            ))
        return super().form_invalid(form)

    def form_valid(self, form):
        Contact(
            email=form.cleaned_data["email"],
            message=form.cleaned_data["message"]
        ).save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _(
            """
            Thanks for contacting First Pick Homeschool!
            We appreciate you reaching out to us and we will get back to you soon.
            """
        ))
        return reverse("home")
