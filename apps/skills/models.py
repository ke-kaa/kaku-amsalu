from django.db import models
from ordered_model.models import OrderedModel


class SkillGroup(OrderedModel):
    name = models.CharField(max_length=120)

    class Meta(OrderedModel.Meta):
        verbose_name = "Skill Group"
        verbose_name_plural = "Skill Groups"

    def __str__(self):
        return self.name


class Skill(OrderedModel):
    class TickerRow(models.TextChoices):
        ROW_1 = "ROW_1", "Row 1"
        ROW_2 = "ROW_2", "Row 2"

    group = models.ForeignKey(
        SkillGroup, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=120)
    display_label = models.CharField(max_length=120, blank=True)
    proficiency = models.IntegerField(default=3)
    show_in_ticker = models.BooleanField(default=False)
    ticker_row = models.CharField(
        max_length=8, choices=TickerRow.choices, default=TickerRow.ROW_1
    )

    order_with_respect_to = "group"

    class Meta(OrderedModel.Meta):
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name
