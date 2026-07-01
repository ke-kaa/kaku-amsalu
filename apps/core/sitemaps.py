from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.projects.models import Project


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["one_page", "cinematic"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Project.objects.filter(is_published=True)

    def location(self, obj):
        return reverse("project_detail", kwargs={"slug": obj.slug})


SITEMAPS = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
}
