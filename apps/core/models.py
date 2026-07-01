from django.db import models
from ordered_model.models import OrderedModel
from solo.models import SingletonModel
from tinymce.models import HTMLField


class SiteSettings(SingletonModel):
    site_title = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=120, default="Kaku Amsalu")
    owner_initials = models.CharField(max_length=12, default="K.A.")
    portfolio_year = models.IntegerField(default=2025)
    available_status = models.BooleanField(default=True)
    available_label = models.CharField(max_length=80, default="Available 2025")
    location_short = models.CharField(max_length=120, default="Addis Ababa · ET")
    location_full = models.CharField(max_length=200, default="AAiT, Addis Ababa, ET")
    timezone_label = models.CharField(max_length=20, default="EAT")
    remote_friendly = models.BooleanField(default=True)
    copyright_text = models.CharField(max_length=200, blank=True)
    footer_quip = models.CharField(
        max_length=200, default="Crafted with passion, caffeine & spite."
    )
    cinematic_url_label = models.CharField(max_length=60, default="Cinematic ↗")
    onepage_url_label = models.CharField(max_length=60, default="One Page")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_title or "Site Settings"


class Hero(SingletonModel):
    first_name = models.CharField(max_length=80, default="Kaku")
    last_name = models.CharField(max_length=80, default="Amsalu")
    lede = HTMLField(blank=True)
    eyebrow_text = models.CharField(
        max_length=120, default="Portfolio / 2025 — Volume One"
    )
    role_strip_role = models.TextField(blank=True)
    meta_status = models.CharField(max_length=120, blank=True)
    meta_domain = models.CharField(max_length=120, blank=True)
    meta_location = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Hero"

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or "Hero"


class Badge(OrderedModel):
    hero = models.ForeignKey(
        Hero,
        on_delete=models.CASCADE,
        related_name="badges",
        null=True,
        blank=True,
    )
    label = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)

    order_with_respect_to = "hero"

    class Meta(OrderedModel.Meta):
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

    def __str__(self):
        return self.label


class About(SingletonModel):
    heading = models.CharField(max_length=200, default="Know me more.")
    paragraph_1 = HTMLField(blank=True)
    paragraph_2 = HTMLField(blank=True)
    paragraph_cinematic_1 = HTMLField(blank=True)
    paragraph_cinematic_2 = HTMLField(blank=True)

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"

    def __str__(self):
        return self.heading or "About"


class Fact(OrderedModel):
    about = models.ForeignKey(
        About, on_delete=models.CASCADE, related_name="facts"
    )
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=255)
    is_link = models.BooleanField(default=False)
    link_url = models.URLField(blank=True, null=True)

    order_with_respect_to = "about"

    class Meta(OrderedModel.Meta):
        verbose_name = "Fact"
        verbose_name_plural = "Facts"

    def __str__(self):
        return f"{self.label}: {self.value}"


class ContactInfo(SingletonModel):
    heading = models.CharField(max_length=200, default="Let's get in touch.")
    lead_text = models.TextField(blank=True)
    body_text = HTMLField(blank=True)
    cinematic_lead = models.TextField(blank=True)

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return self.heading or "Contact Info"


class ContactChannel(OrderedModel):
    class Kind(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        PHONE = "PHONE", "Phone"
        LOCATION = "LOCATION", "Location"
        STATUS = "STATUS", "Status"
        SOCIAL = "SOCIAL", "Social"
        CUSTOM = "CUSTOM", "Custom"

    label = models.CharField(max_length=80)
    value = models.CharField(max_length=255)
    href = models.CharField(max_length=255, blank=True)
    kind = models.CharField(
        max_length=10, choices=Kind.choices, default=Kind.CUSTOM
    )
    is_clickable = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Contact Channel"
        verbose_name_plural = "Contact Channels"

    def __str__(self):
        return f"{self.label}: {self.value}"


class NavLink(OrderedModel):
    class Target(models.TextChoices):
        ONEPAGE = "ONEPAGE", "One Page"
        CINEMATIC = "CINEMATIC", "Cinematic"
        BOTH = "BOTH", "Both"

    label = models.CharField(max_length=80)
    anchor = models.CharField(max_length=120, blank=True)
    external_url = models.URLField(blank=True)
    target = models.CharField(
        max_length=10, choices=Target.choices, default=Target.BOTH
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "Nav Link"
        verbose_name_plural = "Nav Links"

    def __str__(self):
        return self.label


class Announcement(OrderedModel):
    message = models.CharField(max_length=255)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.message


class SocialLink(OrderedModel):
    class Platform(models.TextChoices):
        GITHUB = "GITHUB", "GitHub"
        LINKEDIN = "LINKEDIN", "LinkedIn"
        TWITTER = "TWITTER", "Twitter"
        DRIBBBLE = "DRIBBBLE", "Dribbble"
        BEHANCE = "BEHANCE", "Behance"
        EMAIL = "EMAIL", "Email"

    platform = models.CharField(max_length=12, choices=Platform.choices)
    url = models.URLField()
    display_label = models.CharField(max_length=80, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.display_label or self.get_platform_display()


class SEOMetadata(SingletonModel):
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="seo/", null=True, blank=True)
    twitter_handle = models.CharField(max_length=80, blank=True)
    canonical_url = models.URLField(blank=True)
    keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "SEO Metadata"
        verbose_name_plural = "SEO Metadata"

    def __str__(self):
        return self.meta_title or "SEO Metadata"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} <{self.email}>"
