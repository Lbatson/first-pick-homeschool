from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from fphs.utils.views import robots_txt, ContactView

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("robots.txt", robots_txt, name="robots"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "legal/privacy-policy/",
        TemplateView.as_view(template_name="pages/legal/privacy-policy.html"),
        name="privacy_policy",
    ),
    path(
        "legal/terms-of-service/",
        TemplateView.as_view(template_name="pages/legal/terms-of-service.html"),
        name="terms_of_service",
    ),
    path("contact/", ContactView.as_view(), name="contact"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("accounts/", include("allauth.urls")),
    path("users/", include("fphs.users.urls", namespace="users")),
    # Curriculums
    path("curriculums/", include("fphs.curriculums.urls")),
    # Wagtail CMS
    path("cms/", include("wagtail.admin.urls")),
    path("documents/", include("wagtail.documents.urls")),
    path("", include(("wagtail.core.urls", "wagtail"), namespace="wagtail")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        # Email
        path("anymail/", include("anymail.urls")),
    ]

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
