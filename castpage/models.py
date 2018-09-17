from django.db import models
from django.utils import text, timezone

# Create your models here.

nulls = {'default': None, 'blank': True}

class Cast(models.Model):
    """
    Basic Rocky Horror cast info
    """

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    # logo = models.ImageField()
    created_date = models.DateTimeField(default=timezone.now)

    # Social Links
    external_url = models.URLField(**nulls)
    facebook_url = models.URLField(**nulls)
    twitter_user = models.CharField(max_length=15, **nulls)
    instagram_user = models.CharField(max_length=30, **nulls)

    def save(self, *args, **kwargs):
        # Always make the slug match the name
        self.slug = text.slugify(self.name)
        super(Cast, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class PageSection(models.Model):
    """
    Addition content sections beyond the built-ins
    """

    cast = models.ForeignKey('castpage.Cast', on_delete=models.CASCADE, related_name='page_sections')
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title