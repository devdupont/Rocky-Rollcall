"""
Models to build and manage Rocky casts and their home page
"""

from datetime import date
from django.db import models
from django.utils import text, timezone
from sorl.thumbnail import ImageField
from django_cleanup.signals import cleanup_pre_delete

def sorl_delete(**kwargs):
    from sorl.thumbnail import delete
    delete(kwargs['file'])

cleanup_pre_delete.connect(sorl_delete)

nulls = {'default': None, 'blank': True}

def cast_logo(instance, filename: str) -> str:
    """
    Generate cast logo filename from cast slug
    """
    return f"casts/{instance.slug}/logo.{filename.split('.')[-1]}"

class Cast(models.Model):
    """
    Basic Rocky Horror cast info
    """

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    logo = ImageField(blank=True, upload_to=cast_logo, default='../blank_logo.jpg')
    created_date = models.DateTimeField(default=timezone.now)

    managers = models.ManyToManyField('userprofile.Profile', related_name='managed_casts')

    # Social Links
    external_url = models.URLField(**nulls)
    facebook_url = models.URLField(**nulls)
    twitter_user = models.CharField(max_length=15, **nulls)
    instagram_user = models.CharField(max_length=30, **nulls)

    def save(self, *args, **kwargs):
        """
        Add computed values and save model
        """
        # Always make the slug match the name
        self.slug = text.slugify(self.name)
        super(Cast, self).save(*args, **kwargs)

    def is_manager(self, user) -> bool:
        """
        Returns if a user manages a cast by primary key
        """
        # pylint: disable=E1101
        return not user.is_anonymous and self.managers.filter(pk=user.profile.pk)

    @property
    def future_events(self) -> ['Event']:
        """
        Returns cast events happening today or later
        """
        # pylint: disable=E1101
        return self.events.filter(cast=self, date__gte=date.today())

    @property
    def upcoming_events(self) -> ['Event']:
        """
        Returns the first few future events
        """
        return self.future_events[:3]

    def __str__(self) -> str:
        return self.name

class PageSection(models.Model):
    """
    Additional content sections beyond the built-ins
    """

    cast = models.ForeignKey('castpage.Cast', on_delete=models.CASCADE, related_name='page_sections')
    title = models.CharField(max_length=128)
    text = models.TextField()
    order = models.PositiveSmallIntegerField(default=1)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.cast.name} | {self.title}"
