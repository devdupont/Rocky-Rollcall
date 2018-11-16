"""
User management form classes
"""

# django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# library
from bootstrap_datepicker_plus import DatePickerInput
# app
from photos.forms import PhotoForm
from userprofile.models import Photo, Profile

class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    alt = forms.CharField(
        max_length=128,
        label='Display Name',
        help_text='Optional. If given, this will replace your first and last name on the site and in search'
    )
    birth_date = forms.DateField(
        widget=DatePickerInput(format='%Y-%m-%d'),
        help_text='Required. Format: YYYY-MM-DD. Users under 18 will not appear in search. You must be 13+ to sign up'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'alt', 'email', 'birth_date', 'password1', 'password2',)
        help_texts = {
            'first_name': 'Required',
            'last_name': 'Required',
            'email': 'Required. You will receive a validation email',
        }

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class DeleteUserForm(forms.Form):

    username = forms.CharField(max_length=150, help_text='Type your username to confirm deletion')

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'image', 'alt', 'location', 'bio',
            'external_url', 'facebook_url', 'twitter_user', 'instagram_user',
            'show_email', 'searchable',
        )
        help_texts = {
            'alt': 'If given, this will replace your first and last name on your profile and in search',
            'location': 'We recommend using a city name. Ex: "Orlando, FL"',
            'external_url': 'Your personal website URL. Ex: https://myself.com',
            'facebook_url': 'Facebook profile or fan page URL. Ex: https://facebook.com/myself',
            'twitter_user': 'Twitter @username. Ex: myself',
            'instagram_user': 'Instagram @username. Ex: myself',
            'show_email': 'Enabling this will make your email address visible on your public profile',
            'searchable': 'Enabling this makes your profile information searchable. Must be 18+ to appear in search results',
        }

class UserPhotoForm(PhotoForm):

    class Meta(PhotoForm.Meta):
        model = Photo
