from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    deleted_at = models.DateTimeField(
        verbose_name=_("Deleted At"), null=True, blank=True
    )

    class Meta:
        abstract = True
