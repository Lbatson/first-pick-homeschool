from django.http import HttpResponse
from django.middleware.common import CommonMiddleware


class OverrideCommonMiddleware(CommonMiddleware):
    def process_request(self, request):
        # Override to let health check bypass ALLOWED_HOSTS
        if request.path_info == "/health/":
            return HttpResponse("OK")
        else:
            return super().process_request(request)
