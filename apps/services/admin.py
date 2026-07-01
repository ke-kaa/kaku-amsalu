from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from kaku_portfolio.admin import custom_admin_site
from .models import Service


@admin.action(description="Duplicate selected services")
def duplicate_services(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None
        obj.order = None
        obj.save()


@admin.register(Service, site=custom_admin_site)
class ServiceAdmin(OrderedModelAdmin):
    list_display = ("title", "number_label", "stack_label", "is_active",
                    "move_up_down_links")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("title", "description", "stack_label")
    actions = (duplicate_services,)
