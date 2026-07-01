from django.db import models
from ordered_model.models import OrderedModel


class EducationEntry(OrderedModel):
    year_label = models.CharField(max_length=40, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    class Meta(OrderedModel.Meta):
        verbose_name = "Education Entry"
        verbose_name_plural = "Education Entries"

    def __str__(self):
        return f"{self.title} — {self.organization}".strip(" —")


class ExperienceEntry(OrderedModel):
    code_label = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=200)
    stack_label = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Experience Entry"
        verbose_name_plural = "Experience Entries"

    def __str__(self):
        return self.title
