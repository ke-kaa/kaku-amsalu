"""URL configuration for kaku_portfolio project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import TemplateView

from apps.core.sitemaps import SITEMAPS
from apps.core.views import (
    CinematicView,
    ContactSubmitView,
    OnePageView,
    ProjectDetailView,
)
from kaku_portfolio.admin import custom_admin_site

urlpatterns = [
    path("", OnePageView.as_view(), name="one_page"),
    path("cinematic/", CinematicView.as_view(), name="cinematic"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
    path("contact/", ContactSubmitView.as_view(), name="contact_submit"),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("admin/", custom_admin_site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
