"""Idempotent seed of all portfolio content lifted from the two source HTML files.

Skills (SkillGroup / Skill) are intentionally NOT seeded here — they were
populated separately. Re-running this command is safe: singletons are updated
in place and list rows are matched on a natural key via update_or_create.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import (
    About,
    Badge,
    ContactChannel,
    ContactInfo,
    Fact,
    Hero,
    NavLink,
    SEOMetadata,
    SiteSettings,
)
from apps.resume.models import EducationEntry, ExperienceEntry
from apps.services.models import Service
from apps.projects.models import Project, ProjectTag

EMAIL = "amsalukaku122@gmail.com"


class Command(BaseCommand):
    help = "Seed all portfolio sections except skills (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        self._site()
        self._hero()
        self._about()
        self._contact()
        self._navlinks()
        self._seo()
        self._services()
        self._resume()
        self._projects()
        self.stdout.write(self.style.SUCCESS("Portfolio seeded (skills left untouched)."))

    # ── Singletons ────────────────────────────────────────────────────────
    def _site(self):
        s = SiteSettings.get_solo()
        s.site_title = "Kaku Amsalu — Portfolio"
        s.owner_name = "Kaku Amsalu"
        s.owner_initials = "K.A."
        s.portfolio_year = 2025
        s.available_status = True
        s.available_label = "Available 2025"
        s.location_short = "Addis Ababa · ET"
        s.location_full = "AAiT, Addis Ababa, ET"
        s.timezone_label = "EAT"
        s.remote_friendly = True
        # Left blank so the footer composes "© <current year> <owner>" dynamically.
        # Set this in the admin only to override with a fixed string.
        s.copyright_text = ""
        s.footer_quip = "Crafted with passion, caffeine & spite."
        s.cinematic_url_label = "Cinematic ↗"
        s.onepage_url_label = "One Page"
        s.save()

    def _hero(self):
        h = Hero.get_solo()
        h.first_name = "Kaku"
        h.last_name = "Amsalu"
        h.lede = (
            "<strong>Full-stack developer</strong> &amp; fourth-year Software "
            "Engineering student at AAiT. I work across web, mobile, and "
            "AI-adjacent systems — with a bias for clarity, performance, and intent."
        )
        h.eyebrow_text = "Portfolio / 2025 — Volume One"
        h.role_strip_role = (
            "Full-stack developer based in Addis Ababa. Building web, mobile, and "
            "AI-adjacent systems with a bias for clarity, speed, and intent."
        )
        h.meta_status = "Available 2025"
        h.meta_domain = "Web · Mobile · AI"
        h.meta_location = "ET / Remote"
        h.save()
        for order, label in enumerate(
            ["Available 2025", "Addis Ababa · ET", "Remote-friendly"]
        ):
            Badge.objects.update_or_create(
                hero=h, label=label, defaults={"is_active": True}
            )

    def _about(self):
        a = About.get_solo()
        a.heading = "Know me more."
        a.paragraph_1 = (
            "<p>I'm <strong>Kaku Amsalu</strong>, a fourth-year Software Engineering "
            "student at Addis Ababa University. I build web and mobile products with a "
            "growing focus on AI-driven systems — caring about intuitive interfaces, "
            "performant backends, and the small details that make software feel "
            "inevitable.</p>"
        )
        a.paragraph_2 = (
            "<p>Currently going deep on distributed systems, message brokers, and "
            "cloud-native architecture through the ALX Pro Backend and AWS Cloud "
            "Computing programs.</p>"
        )
        a.paragraph_cinematic_1 = (
            "Fourth-year Software Engineering student at Addis Ababa University. I work "
            "across web and mobile, with a growing focus on AI-driven systems. I care "
            "about intuitive interfaces, performant backends, and the small details "
            "that make software feel inevitable rather than assembled."
        )
        a.paragraph_cinematic_2 = (
            "I'm continuously learning — currently deep in distributed systems, "
            "message brokers, and cloud-native architecture."
        )
        a.save()
        facts = [
            ("Name", "Kaku Amsalu", False, ""),
            ("Email", EMAIL, True, f"mailto:{EMAIL}"),
            ("Based in", "Addis Ababa, ET", False, ""),
            ("Studying", "AAiT — SWE", False, ""),
        ]
        for label, value, is_link, url in facts:
            Fact.objects.update_or_create(
                about=a,
                label=label,
                defaults={"value": value, "is_link": is_link, "link_url": url or None},
            )

    def _contact(self):
        c = ContactInfo.get_solo()
        c.heading = "Let's get in touch."
        c.lead_text = (
            "Always eager to collaborate on web, mobile, or AI projects that make a "
            "difference. Looking for someone passionate, dedicated, and ready to "
            "contribute? Let's build something impactful."
        )
        c.cinematic_lead = "End of index.<br/>New project? Open question?<br/>The line is open."
        c.save()
        channels = [
            ("Email", EMAIL, f"mailto:{EMAIL}", ContactChannel.Kind.EMAIL, True),
            ("Phone", "+251 972 489 050", "tel:+251972489050", ContactChannel.Kind.PHONE, True),
            ("Location", "AAiT, Addis Ababa, ET", "", ContactChannel.Kind.LOCATION, False),
            ("Status", "Available · 2025", "", ContactChannel.Kind.STATUS, False),
        ]
        for label, value, href, kind, clickable in channels:
            ContactChannel.objects.update_or_create(
                label=label,
                defaults={"value": value, "href": href, "kind": kind, "is_clickable": clickable},
            )

    def _navlinks(self):
        links = [
            ("About", "#about"),
            ("Services", "#services"),
            ("Resume", "#resume"),
            ("Skills", "#skills"),
            ("Work", "#projects"),
            ("Contact", "#contact"),
        ]
        for label, anchor in links:
            NavLink.objects.update_or_create(
                label=label,
                defaults={"anchor": anchor, "target": NavLink.Target.ONEPAGE},
            )

    def _seo(self):
        seo = SEOMetadata.get_solo()
        seo.meta_title = "Kaku Amsalu — Full-Stack Developer"
        seo.meta_description = (
            "Full-stack developer & Software Engineering student at AAiT, building "
            "web, mobile, and AI-adjacent systems."
        )
        seo.keywords = "Kaku Amsalu, full-stack developer, Django, React, Flutter, Addis Ababa"
        seo.save()

    # ── Lists ─────────────────────────────────────────────────────────────
    def _services(self):
        Service.objects.filter(title__iexact="test").delete()  # remove placeholder
        services = [
            ("/ 01", "Frontend Development", "Frontend<br/>Development",
             "Responsive interfaces in React with Tailwind. Clean code, accessibility, "
             "and seamless interactions across devices.", "React · Tailwind · TypeScript"),
            ("/ 02", "Backend Development", "Backend<br/>Development",
             "Scalable, secure systems with Django, Node, Firebase. Auth, validation, "
             "real-time data, integrations, DB tuning.", "Django · Node · Firebase"),
            ("/ 03", "Mobile Development", "Mobile<br/>Development",
             "Cross-platform apps in Flutter with native-feel performance. State "
             "management, offline support, agile delivery.", "Flutter · iOS · Android"),
            ("/ 04", "UI / UX Design", "UI/UX<br/>Design",
             "User-centric interfaces in Figma. Pixel-perfect prototypes, consistent "
             "design systems, journey mapping.", "Figma · Systems · Prototyping"),
        ]
        for num, title, brk, desc, stack in services:
            Service.objects.update_or_create(
                title=title,
                defaults={"number_label": num, "title_break": brk,
                          "description": desc, "stack_label": stack, "is_active": True},
            )

    def _resume(self):
        education = [
            ("22 — 27", 2022, 2027, "BSc Software Engineering", "Addis Ababa University",
             "Systematic software development, algorithmic problem-solving, and software "
             "design patterns. Applied through hands-on projects.", True),
            ("24 — 25", 2024, 2025, "Backend Development", "ALX Ethiopia",
             "RESTful APIs in Django, MySQL schema design, JWT/OAuth, and CI/CD pipelines "
             "for automated deployment.", False),
            ("25 — 26", 2025, 2026, "Pro Backend Development", "ALX Ethiopia",
             "Microservices, Docker, distributed systems, message brokers "
             "(RabbitMQ / Kafka), and cloud-native applications.", False),
            ("25 — 26", 2025, 2026, "AWS Cloud Computing", "ALX Ethiopia",
             "AWS Well-Architected Framework — fault-tolerant architectures with EC2, "
             "S3, RDS, Lambda; cost & security optimization.", False),
        ]
        for yr, start, end, title, org, desc, current in education:
            EducationEntry.objects.update_or_create(
                title=title, organization=org,
                defaults={"year_label": yr, "start_year": start, "end_year": end,
                          "description": desc, "is_current": current},
            )
        experience = [
            ("/ FE", "Front End Developer", "React · Redux · Styled",
             "Dynamic, responsive interfaces with state management, accessibility "
             "(WCAG), and cross-browser compatibility."),
            ("/ BE", "Backend Developer", "Node · Django · AWS",
             "Scalable server architecture, RESTful APIs, SQL/NoSQL design, OAuth/JWT "
             "flows, caching, cloud deployment."),
            ("/ UX", "UI / UX Designer", "Figma · Atomic · Systems",
             "User-centered design, wireframing, prototyping, usability testing. Atomic "
             "design systems balancing aesthetic and feasibility."),
            ("/ MO", "Mobile Application Developer", "Flutter · CI/CD",
             "Cross-platform performance with native module integration, "
             "platform-specific UX, optimized for device constraints."),
        ]
        for code, title, stack, desc in experience:
            ExperienceEntry.objects.update_or_create(
                title=title,
                defaults={"code_label": code, "stack_label": stack, "description": desc},
            )

    def _projects(self):
        projects = [
            dict(slug="medimap", number_label="№ 01", project_number=1, title="MediMap",
                 title_break="", category="Web · GIS · Health-Tech", frame_variant="MEDIMAP",
                 frame_tag="PostGIS", frame_subtitle="Geospatial Pharmacy Index", year=2024,
                 description_short="Search medicines, view nearby pharmacies with real-time "
                 "stock, and discover via map-based UI with pharmacy inventory management.",
                 tags=["Django", "DRF", "React", "PostgreSQL", "PostGIS"]),
            dict(slug="github-analyzer", number_label="№ 02", project_number=2,
                 title="GitHub Analyzer", title_break="GitHub<br/>Analyzer",
                 category="Web · Data · Tooling", frame_variant="GITHUB", frame_tag="REST",
                 frame_subtitle="Profile / Repo / Language Insights", year=2024,
                 description_short="Search any GitHub user, browse their repositories, and "
                 "visualize language usage and profile metadata.",
                 tags=["React", "Redux", "CSS", "REST API"]),
            dict(slug="airbnb-backend-clone", number_label="№ 03", project_number=3,
                 title="Airbnb Backend Clone", title_break="Airbnb<br/>Backend",
                 category="Backend · API · Marketplace", frame_variant="AIRBNB",
                 frame_tag="GraphQL", frame_subtitle="REST + GraphQL · Modular", year=2024,
                 description_short="Auth, listings, bookings, payments, reviews. Robust, "
                 "scalable, modular — exposed via both REST and GraphQL.",
                 tags=["Django", "DRF", "GraphQL", "Celery", "Redis", "Docker", "Swagger"]),
            dict(slug="escrow-api", number_label="№ 04", project_number=4, title="Escrow API",
                 title_break="Escrow<br/>API", category="Backend · FinTech · Workflow",
                 frame_variant="ESCROW", frame_tag="Stripe",
                 frame_subtitle="Client · Freelancer · Admin", year=2024,
                 description_short="Escrow-based freelance payments with disputes and audit "
                 "logs. Role-based access, Stripe handling, fully documented.",
                 tags=["Django", "DRF", "PostgreSQL", "Celery", "Redis", "Swagger"]),
            dict(slug="timesheet-leave", number_label="№ 05", project_number=5,
                 title="Timesheet & Leave", title_break="Timesheet<br/>&amp; Leave",
                 category="Backend · HR · Internal Tools", frame_variant="TIMESHEET",
                 frame_tag="RBAC", frame_subtitle="Employee · Manager · Admin", year=2025,
                 description_short="Track attendance, manage leave requests, and generate "
                 "reports. Three roles (employee / manager / admin) with secure backend.",
                 tags=["Django", "DRF", "GraphQL", "Celery", "Redis", "Docker", "Swagger"]),
        ]
        for data in projects:
            tags = data.pop("tags")
            data["role_label"] = data["category"]
            data["version_label"] = "v1"
            data["is_published"] = True
            project, _ = Project.objects.update_or_create(
                slug=data["slug"], defaults=data
            )
            for label in tags:
                ProjectTag.objects.update_or_create(project=project, label=label)
