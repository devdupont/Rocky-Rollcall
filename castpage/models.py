"""
Models to build and manage Rocky casts and their home page
"""

from datetime import date
from django.db import models
from django.utils import text, timezone
from sorl.thumbnail import ImageField
from tinymce.models import HTMLField
from photos.models import PhotoBase

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
    members = models.ManyToManyField('userprofile.Profile', related_name='member_casts')
    member_requests = models.ManyToManyField('userprofile.Profile', related_name='requested_casts')
    blocked = models.ManyToManyField('userprofile.Profile', related_name='blocked_casts')

    # Social Links
    external_url = models.URLField(blank=True, verbose_name='Existing Homepage')
    facebook_url = models.URLField(blank=True, verbose_name='Facebook Group URL')
    twitter_user = models.CharField(max_length=15, blank=True, verbose_name='Twitter Username')
    instagram_user = models.CharField(max_length=30, blank=True, verbose_name='Instagram Username')

    def save(self, *args, **kwargs):
        """
        Add computed values and save model
        """
        # Always make the slug match the name
        self.slug = text.slugify(self.name)
        super(Cast, self).save(*args, **kwargs)

    def add_manager(self, profile: 'userprofile.Profile'):
        """
        Adds a new profile to managers or raises an error
        """
        if self.managers.filter(pk=profile.pk):
            raise ValueError(f'{profile} is already a manager of {self}')
        if not self.members.filter(pk=profile.pk):
            raise ValueError(f'{profile} is not a member of {self}')
        self.managers.add(profile)

    def remove_manager(self, profile: 'userprofile.Profile'):
        """
        Remove a profile from managers
        """
        if not self.managers.filter(pk=profile.pk):
            raise ValueError(f'{profile} is not a manager or {self}')
        self.managers.remove(profile) # pylint: disable=E1101

    def is_manager(self, user: 'auth.User') -> bool:
        """
        Returns if a user manages a cast by primary key
        """
        return not user.is_anonymous and self.managers.filter(pk=user.profile.pk)

    @property
    def managers_as_user(self) -> ['auth.User']:
        """
        Returns managers as a list of auth Users
        """
        return [u.user for u in self.managers.all()]

    def add_member_request(self, profile: 'userprofile.Profile'):
        """
        Adds a new profile to membership requests or raises an error
        """
        if self.members.filter(pk=profile.pk):
            raise ValueError(f'{profile} is already a member of {self}')
        if self.member_requests.filter(pk=profile.pk):
            raise ValueError(f'{profile} has already requested to join {self}')
        if self.blocked.filter(pk=profile.pk):
            raise ValueError(f'{profile} is blocked from joining {self}')
        self.member_requests.add(profile)

    def remove_member_request(self, profile: 'userprofile.Profile'):
        """
        Removes a profile from membership requests
        """
        if not self.member_requests.filter(pk=profile.pk):
            raise ValueError(f'{profile} has not requested to join {self}')
        self.member_requests.remove(profile) # pylint: disable=E1101

    def add_member(self, profile: 'userprofile.Profile'):
        """
        Adds a new profile to members or raises an error
        """
        if self.members.filter(pk=profile.pk):
            raise ValueError(f'{profile} is already a member of {self}')
        self.members.add(profile)

    def remove_member(self, profile: 'userprofile.Profile'):
        """
        Remove a profile from members
        """
        if self.managers.filter(pk=profile.pk):
            raise ValueError(f'{profile} cannot be removed because they are a manager of {self}')
        if not self.members.filter(pk=profile.pk):
            raise ValueError(f'{profile} is not a member or {self}')
        self.members.remove(profile) # pylint: disable=E1101

    @property
    def future_events(self) -> ['Event']:
        """
        Returns cast events happening today or later
        """
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
