"""
Models to build and manage User profiles and settings
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from castpage.models import PhotoBase

def profile_image(instance, filename: str) -> str:
    """
    Generate cast logo filename from cast slug
    """
    return f"users/{instance.user.username}/profile_image.{filename.split('.')[-1]}"

class Profile(models.Model):
    """
    Profile info to add on top of the auth.User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Public Profile
    image = ImageField(blank=True, upload_to=profile_image, verbose_name='Profile Photo')
    alt = models.CharField(max_length=128, blank=True, verbose_name='Stage Name')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Public Bio')
    location = models.CharField(max_length=64, blank=True)

    # Config
    email_confirmed = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

    def save_from_form(self, form: 'SignUpForm'):
        """
        Assign profile attrs from new user form
        """
        self.birth_date = form.cleaned_data.get('birth_date')
        self.alt = form.cleaned_data.get('alt')

    def __str__(self):
        return self.user.username #pylint: disable=E1101

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a profile for a new User model
    """
    if created:
        Profile.objects.create(user=instance) #pylint: disable=E1101
    instance.profile.save()

class UserPhoto(PhotoBase):
    """
    Photos associated with a user profile
    """

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
