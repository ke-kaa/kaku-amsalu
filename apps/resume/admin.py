from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from kaku_portfolio.admin import custom_admin_site
from .models import EducationEntry, ExperienceEntry


@admin.register(EducationEntry, site=custom_admin_site)
class EducationEntryAdmin(OrderedModelAdmin):
    list_display = ("title", "organization", "year_label", "is_current",
                    "move_up_down_links")
    list_filter = ("is_current",)
    list_editable = ("is_current",)
    search_fields = ("title", "organization", "description")


@admin.register(ExperienceEntry, site=custom_admin_site)
class ExperienceEntryAdmin(OrderedModelAdmin):
    list_display = ("title", "code_label", "stack_label", "move_up_down_links")
    search_fields = ("title", "stack_label", "description")
