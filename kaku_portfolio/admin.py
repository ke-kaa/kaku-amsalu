"""Custom admin site with a function-grouped sidebar (PLAN_03 work item E)."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Sidebar groups: "App.Model" identifiers, in display order.
# Inline-only models (Badge, Fact, Skill, ProjectTag/Meta/GalleryImage) are not
# registered standalone, so they are intentionally absent.
GROUPS = {
    "Identity": [
        "core.SiteSettings",
        "core.Hero",
        "core.About",
        "core.ContactInfo",
        "core.ContactChannel",
    ],
    "Content": [
        "services.Service",
        "resume.EducationEntry",
        "resume.ExperienceEntry",
        "skills.SkillGroup",
        "projects.Project",
    ],
    "Site": [
        "core.NavLink",
        "core.SocialLink",
        "core.Announcement",
        "core.SEOMetadata",
    ],
    "Inbox": [
        "core.ContactSubmission",
    ],
}

# Any registered model not named above lands here, so nothing disappears.
CATCHALL_GROUP = "Administration"


class CustomAdminSite(admin.AdminSite):
    site_header = "Kaku Portfolio CMS"
    site_title = "Kaku Portfolio CMS"
    index_title = "Content Management"

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            return []

        # Flatten every model the user may see, keyed "app_label.ObjectName".
        available = {}
        for app in app_dict.values():
            for model in app["models"]:
                key = f"{app['app_label']}.{model['object_name']}"
                available[key] = model

        grouped = set()
        app_list = []
        for group_name, identifiers in GROUPS.items():
            models = []
            for ident in identifiers:
                model = available.get(ident)
                if model:
                    models.append(model)
                    grouped.add(ident)
            if models:
                app_list.append({
                    "name": group_name,
                    "app_label": group_name.lower().replace(" ", "_"),
                    "app_url": "",
                    "has_module_perms": True,
                    "models": models,
                })

        # Catch-all for anything not explicitly grouped (e.g. auth.User).
        leftovers = [m for k, m in available.items() if k not in grouped]
        if leftovers:
            app_list.append({
                "name": CATCHALL_GROUP,
                "app_label": "administration",
                "app_url": "",
                "has_module_perms": True,
                "models": sorted(leftovers, key=lambda m: m["name"]),
            })

        return app_list


custom_admin_site = CustomAdminSite(name="custom_admin")

# Auth: a custom site does not inherit the default site's registrations, so
# register the User model explicitly (single operator — Group is omitted).
custom_admin_site.register(User, UserAdmin)
