from django.contrib import admin
from django.db import transaction
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)

from kaku_portfolio.admin import custom_admin_site
from .models import (
    Project,
    ProjectGalleryImage,
    ProjectMeta,
    ProjectTag,
)


class ProjectTagInline(OrderedTabularInline):
    model = ProjectTag
    fields = ("label", "order", "move_up_down_links")
    readonly_fields = ("order", "move_up_down_links")
    extra = 0
    ordering = ("order",)


class ProjectMetaInline(OrderedTabularInline):
    model = ProjectMeta
    fields = ("key", "value", "position", "order", "move_up_down_links")
    readonly_fields = ("order", "move_up_down_links")
    extra = 0
    ordering = ("order",)


class ProjectGalleryImageInline(OrderedTabularInline):
    model = ProjectGalleryImage
    fields = ("image", "caption", "order", "move_up_down_links")
    readonly_fields = ("order", "move_up_down_links")
    extra = 0
    ordering = ("order",)


@admin.action(description="Duplicate selected projects (shallow)")
def duplicate_projects(modeladmin, request, queryset):
    for obj in queryset:
        tags = list(obj.tags.all())
        metas = list(obj.meta_lines.all())
        gallery = list(obj.gallery.all())
        with transaction.atomic():
            obj.pk = None 
            obj.order = None
            obj.slug = f"{obj.slug}-copy"
            obj.is_published = False
            obj.save()
            for child_list in (tags, metas, gallery):
                for c in child_list:
                    c.pk = None
                    c.order = None
                    c.project = obj
                    c.save()

@admin.register(Project, site=custom_admin_site)
class ProjectAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ("title", "number_label", "category", "year",
                    "is_featured", "is_published", "move_up_down_links")
    list_filter = ("is_featured", "is_published", "category", "frame_variant")
    list_editable = ("is_featured", "is_published")
    search_fields = ("title", "description_short", "description_long")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ProjectTagInline, ProjectMetaInline, ProjectGalleryImageInline)
    actions = (duplicate_projects,)
    fieldsets = (
        ("Identity", {
            "fields": ("title", "title_break", "slug", "number_label",
                       "project_number", "category", "year"),
        }),
        ("Copy", {
            "fields": ("role_label", "description_short", "description_long"),
        }),
        ("Frame", {
            "fields": ("frame_variant", "frame_tag", "frame_subtitle",
                       "version_label", "footer_left", "cover_image"),
        }),
        ("Links", {
            "fields": ("live_url", "repo_url", "case_study_url"),
        }),
        ("Flags", {
            "fields": ("is_featured", "is_published"),
        }),
    )
