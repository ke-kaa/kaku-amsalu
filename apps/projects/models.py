from django.db import models
from ordered_model.models import OrderedModel
from tinymce.models import HTMLField


class Project(OrderedModel):
    class FrameVariant(models.TextChoices):
        MEDIMAP = "MEDIMAP", "MediMap"
        GITHUB = "GITHUB", "GitHub"
        AIRBNB = "AIRBNB", "Airbnb"
        ESCROW = "ESCROW", "Escrow"
        TIMESHEET = "TIMESHEET", "Timesheet"
        CUSTOM = "CUSTOM", "Custom"

    slug = models.SlugField(max_length=120, unique=True)
    number_label = models.CharField(max_length=20, blank=True)
    project_number = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    title_break = models.CharField(max_length=200, blank=True)
    role_label = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=120, blank=True)
    description_short = models.TextField(blank=True)
    description_long = HTMLField(blank=True)
    year = models.IntegerField(null=True, blank=True)
    frame_variant = models.CharField(
        max_length=12, choices=FrameVariant.choices, default=FrameVariant.CUSTOM
    )
    frame_tag = models.CharField(max_length=80, blank=True)
    frame_subtitle = models.CharField(max_length=200, blank=True)
    version_label = models.CharField(max_length=20, blank=True)
    footer_left = models.CharField(max_length=200, blank=True)
    cover_image = models.ImageField(upload_to="projects/", null=True, blank=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    case_study_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class ProjectTag(OrderedModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tags"
    )
    label = models.CharField(max_length=80)

    order_with_respect_to = "project"

    class Meta(OrderedModel.Meta):
        verbose_name = "Project Tag"
        verbose_name_plural = "Project Tags"

    def __str__(self):
        return self.label


class ProjectMeta(OrderedModel):
    class Position(models.TextChoices):
        TOP_LEFT = "TOP_LEFT", "Top Left"
        TOP_RIGHT = "TOP_RIGHT", "Top Right"

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="meta_lines"
    )
    key = models.CharField(max_length=80)
    value = models.CharField(max_length=120)
    position = models.CharField(
        max_length=10, choices=Position.choices, default=Position.TOP_LEFT
    )

    order_with_respect_to = "project"

    class Meta(OrderedModel.Meta):
        verbose_name = "Project Meta"
        verbose_name_plural = "Project Meta"

    def __str__(self):
        return f"{self.key}: {self.value}"


class ProjectGalleryImage(OrderedModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)

    order_with_respect_to = "project"

    class Meta(OrderedModel.Meta):
        verbose_name = "Project Gallery Image"
        verbose_name_plural = "Project Gallery Images"

    def __str__(self):
        return self.caption or f"Image #{self.pk}"
