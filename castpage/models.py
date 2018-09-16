from django.db import models
from django.utils.text import slugify

# Create your models here.

class Cast(models.Model):
    """
    Basic Rocky Horror cast info
    """

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField()
    # logo = models.ImageField()
    external_url = models.URLField()

    # Social Links
    facebook_url = models.URLField()
    twitter_user = models.CharField(max_length=15)
    instagram_user = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        # Always make the slug match the name
        self.slug = slugify(self.name)
        super(Cast, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
