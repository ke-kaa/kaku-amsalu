from django.contrib import admin
from ordered_model.admin import (
    OrderedInlineModelAdminMixin,
    OrderedModelAdmin,
    OrderedTabularInline,
)

from kaku_portfolio.admin import custom_admin_site
from .models import Skill, SkillGroup


class SkillInline(OrderedTabularInline):
    model = Skill
    fields = ("name", "display_label", "show_in_ticker", "ticker_row",
              "order", "move_up_down_links")
    readonly_fields = ("order", "move_up_down_links")
    extra = 0
    ordering = ("order",)


@admin.register(SkillGroup, site=custom_admin_site)
class SkillGroupAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ("name", "move_up_down_links")
    search_fields = ("name",)
    inlines = (SkillInline,)
