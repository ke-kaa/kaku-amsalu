from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)
from solo.admin import SingletonModelAdmin

from kaku_portfolio.admin import custom_admin_site
from .models import (
    About,
    Announcement,
    Badge,
    ContactChannel,
    ContactInfo,
    ContactSubmission,
    Fact,
    Hero,
    NavLink,
    SEOMetadata,
    SiteSettings,
    SocialLink,
)

# Site header/title/index_title are defined on CustomAdminSite itself.


# --- Inlines -----------------------------------------------------------------

class BadgeInline(OrderedTabularInline):
    model = Badge
    fields = ("label", "is_active", "order", "move_up_down_links")
    readonly_fields = ("order", "move_up_down_links")
    extra = 0
    ordering = ("order",)


class FactInline(OrderedTabularInline):
    model = Fact
    fields = ("label", "value", "is_link", "link_url", "order", "move_up_down_links")
    readonly_fields = ("order", "move_up_down_links")
    extra = 0
    ordering = ("order",)


# --- Singletons --------------------------------------------------------------

@admin.register(SiteSettings, site=custom_admin_site)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ("Identity", {
            "fields": ("site_title", "owner_name", "owner_initials", "portfolio_year"),
        }),
        ("Availability", {
            "fields": ("available_status", "available_label", "remote_friendly"),
        }),
        ("Location", {
            "fields": ("location_short", "location_full", "timezone_label"),
        }),
        ("Footer & Labels", {
            "fields": ("copyright_text", "footer_quip",
                       "cinematic_url_label", "onepage_url_label"),
        }),
    )


@admin.register(Hero, site=custom_admin_site)
class HeroAdmin(OrderedInlineModelAdminMixin, SingletonModelAdmin):
    inlines = (BadgeInline,)
    fieldsets = (
        ("Name", {"fields": ("first_name", "last_name")}),
        ("Copy", {"fields": ("lede", "eyebrow_text", "role_strip_role")}),
        ("Meta strip", {"fields": ("meta_status", "meta_domain", "meta_location")}),
    )


@admin.register(About, site=custom_admin_site)
class AboutAdmin(OrderedInlineModelAdminMixin, SingletonModelAdmin):
    inlines = (FactInline,)
    fieldsets = (
        ("Heading", {"fields": ("heading",)}),
        ("One Page", {"fields": ("paragraph_1", "paragraph_2")}),
        ("Cinematic", {"fields": ("paragraph_cinematic_1", "paragraph_cinematic_2")}),
    )


@admin.register(ContactInfo, site=custom_admin_site)
class ContactInfoAdmin(SingletonModelAdmin):
    fieldsets = (
        ("Heading", {"fields": ("heading",)}),
        ("One Page", {"fields": ("lead_text", "body_text")}),
        ("Cinematic", {"fields": ("cinematic_lead",)}),
    )


@admin.register(SEOMetadata, site=custom_admin_site)
class SEOMetadataAdmin(SingletonModelAdmin):
    fieldsets = (
        ("Meta", {"fields": ("meta_title", "meta_description", "keywords")}),
        ("Social", {"fields": ("og_image", "twitter_handle", "canonical_url")}),
    )


# --- Orderable lists ---------------------------------------------------------

@admin.register(ContactChannel, site=custom_admin_site)
class ContactChannelAdmin(OrderedModelAdmin):
    list_display = ("label", "kind", "value", "is_clickable", "move_up_down_links")
    list_filter = ("kind", "is_clickable")
    list_editable = ("is_clickable",)
    search_fields = ("label", "value")


@admin.register(NavLink, site=custom_admin_site)
class NavLinkAdmin(OrderedModelAdmin):
    list_display = ("label", "target", "anchor", "external_url", "move_up_down_links")
    list_filter = ("target",)
    search_fields = ("label", "anchor")


@admin.register(Announcement, site=custom_admin_site)
class AnnouncementAdmin(OrderedModelAdmin):
    list_display = ("message", "is_active", "start_at", "end_at", "move_up_down_links")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("message",)


@admin.register(SocialLink, site=custom_admin_site)
class SocialLinkAdmin(OrderedModelAdmin):
    list_display = ("platform", "display_label", "url", "move_up_down_links")
    list_filter = ("platform",)
    search_fields = ("display_label", "url")


# --- Inbox -------------------------------------------------------------------

@admin.action(description="Mark selected as read")
def mark_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.register(ContactSubmission, site=custom_admin_site)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read", "replied_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message",
                       "created_at", "ip_address", "user_agent")
    date_hierarchy = "created_at"
    actions = (mark_read,)
