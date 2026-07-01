from django.db import models
from ordered_model.models import OrderedModel


class Service(OrderedModel):
    number_label = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=120)
    title_break = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    stack_label = models.CharField(max_length=200, blank=True)
    icon = models.ImageField(upload_to="services/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta(OrderedModel.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title
