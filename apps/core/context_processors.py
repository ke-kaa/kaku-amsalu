"""Site-wide template globals injected into every request."""

from django.db.models import Q
from django.utils import timezone

from .models import Announcement, NavLink, SEOMetadata, SiteSettings, SocialLink


def site_globals(request):
    now = timezone.now()
    active_announcements = (
        Announcement.objects.filter(is_active=True)
        .filter(Q(start_at__isnull=True) | Q(start_at__lte=now))
        .filter(Q(end_at__isnull=True) | Q(end_at__gte=now))
    )
    return {
        "site": SiteSettings.get_solo(),
        "seo": SEOMetadata.get_solo(),
        "socials": SocialLink.objects.all(),
        "nav_links": NavLink.objects.all(),  # views may override with a page-filtered set
        "announcements": active_announcements,
        "current_year": now.year,
    }
