from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormView

from apps.projects.models import Project
from apps.resume.models import EducationEntry, ExperienceEntry
from apps.services.models import Service
from apps.skills.models import Skill, SkillGroup

from .forms import ContactForm
from .models import About, ContactChannel, ContactInfo, Hero, NavLink


class PortfolioContextMixin(ContextMixin):
    """Shared context for both portfolio pages.

    Set ``page_target`` to ``NavLink.Target.ONEPAGE`` / ``CINEMATIC`` so the nav
    is filtered to the links meant for that page (plus BOTH).
    """

    page_target = None

    def _preview(self):
        """Staff + ?preview=1 → include unpublished/inactive content."""
        return bool(
            self.request.GET.get("preview") and self.request.user.is_staff
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        preview = self._preview()

        services = Service.objects.all()
        projects = Project.objects.prefetch_related("tags", "meta_lines", "gallery")
        if not preview:
            services = services.filter(is_active=True)
            projects = projects.filter(is_published=True)

        ctx.update({
            "hero": Hero.get_solo(),
            "about": About.get_solo(),
            "contact": ContactInfo.get_solo(),
            "services": services,
            "education": EducationEntry.objects.all(),
            "experience": ExperienceEntry.objects.all(),
            "skill_groups": SkillGroup.objects.prefetch_related("skills"),
            "ticker_row1": Skill.objects.filter(
                show_in_ticker=True, ticker_row=Skill.TickerRow.ROW_1
            ),
            "ticker_row2": Skill.objects.filter(
                show_in_ticker=True, ticker_row=Skill.TickerRow.ROW_2
            ),
            "projects": projects,
            "contact_channels": ContactChannel.objects.all(),
            "contact_form": ContactForm(),
        })

        if self.page_target:
            ctx["nav_links"] = NavLink.objects.filter(
                target__in=[self.page_target, NavLink.Target.BOTH]
            )
        return ctx


class OnePageView(PortfolioContextMixin, TemplateView):
    template_name = "one_page.html"
    page_target = NavLink.Target.ONEPAGE


class CinematicView(PortfolioContextMixin, TemplateView):
    template_name = "cinematic.html"
    page_target = NavLink.Target.CINEMATIC


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("tags", "meta_lines", "gallery")
        if not (self.request.GET.get("preview") and self.request.user.is_staff):
            qs = qs.filter(is_published=True)
        return qs


class ContactSubmitView(PortfolioContextMixin, FormView):
    """Handles the contact form POST from either page.

    Inherits the full page context so an invalid submit re-renders the whole
    originating page (with the bound form's errors), not a blank shell. The
    page is chosen from a validated ``next`` field so a cinematic submit
    returns to cinematic and a one-page submit returns to one-page.
    """

    form_class = ContactForm
    page_target = NavLink.Target.ONEPAGE

    def _origin(self):
        nxt = self.request.POST.get("next") or self.request.GET.get("next") or ""
        allowed = {reverse("one_page"), reverse("cinematic")}
        return nxt if nxt in allowed else reverse("one_page")

    def get_template_names(self):
        if self._origin() == reverse("cinematic"):
            return ["cinematic.html"]
        return ["one_page.html"]

    def get_success_url(self):
        return f"{self._origin()}?sent=1#contact"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # The template renders `contact_form`; on error show the bound form.
        ctx["contact_form"] = ctx.get("form")
        return ctx

    def form_valid(self, form):
        # Honeypot tripped → pretend success, save nothing, send nothing.
        if form.is_spam():
            return super().form_valid(form)

        submission = form.save(commit=False)
        submission.ip_address = self.request.META.get("REMOTE_ADDR")
        submission.user_agent = self.request.META.get("HTTP_USER_AGENT", "")[:255]
        submission.save()
        self._notify_owner(submission)
        messages.success(self.request, "Thanks — your message has been sent.")
        return super().form_valid(form)

    def _notify_owner(self, submission):
        """Email the owner. Never let a mail failure lose a saved submission."""
        try:
            send_mail(
                subject=f"Portfolio contact: {submission.subject or '(no subject)'}",
                message=(
                    f"From: {submission.name} <{submission.email}>\n\n"
                    f"{submission.message}\n\n"
                    f"— IP {submission.ip_address}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
        except Exception:  # pragma: no cover - defensive; submission already saved
            pass
