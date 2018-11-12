"""
Models to build and manage Rocky casts and their home page
"""

from datetime import date
from django.db import models
from django.utils import text, timezone
from sorl.thumbnail import ImageField
from django_cleanup.signals import cleanup_pre_delete
from tinymce.models import HTMLField
from photos.models import PhotoBase

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

def cast_photo(instance, filename: str) -> str:
    """
    Generate cast photo filename from cast slug
    """
    return f"casts/{instance.cast.slug}/photos/{filename}"

class Cast(models.Model):
    """
    Basic Rocky Horror cast info
    """

    name = models.CharField(max_length=128, unique=True, verbose_name='Cast Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = HTMLField(verbose_name='About Us')
    logo = ImageField(blank=True, upload_to=cast_logo, verbose_name='Cast Logo')
    email = models.EmailField(max_length=128, verbose_name='Contact Email')
    created_date = models.DateTimeField(default=timezone.now)

    managers = models.ManyToManyField('userprofile.Profile', related_name='managed_casts')

    # Social Links
    external_url = models.URLField(**nulls, verbose_name='Existing Homepage')
    facebook_url = models.URLField(**nulls, verbose_name='Facebook Group URL')
    twitter_user = models.CharField(max_length=15, **nulls, verbose_name='Twitter Username')
    instagram_user = models.CharField(max_length=30, **nulls, verbose_name='Instagram Username')

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
    def managers_as_user(self) -> ['auth.User']:
        """
        Returns managers as a list of auth Users
        """
        return [u.user for u in self.managers.all()] # pylint: disable=E1101

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
    title = models.CharField(max_length=128, verbose_name='Section Title')
    text = HTMLField(verbose_name='Content')
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Section Priority')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.cast.name} | {self.title}"

class Photo(PhotoBase):
    """
    Photos associated with a cast profile
    """

    cast = models.ForeignKey('castpage.Cast', on_delete=models.CASCADE, related_name='photos')
    image = ImageField(upload_to=cast_photo)
