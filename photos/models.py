from django.db import models
from django.utils import timezone
from sorl.thumbnail import ImageField

class PhotoBase(models.Model):
    """
    Base Photo class
    """

    description = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ['-pk']
