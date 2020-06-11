from urllib.parse import urlparse

from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    isProd = request.get_host().split('.')[0] == "firstpickhomeschool"
    lines = [
        "User-Agent: *",
        f"Disallow: {'/admin' if isProd else '/'}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
