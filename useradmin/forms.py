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
from userprofile.models import Profile

class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    alt = forms.CharField(max_length=128, label='Display Name')
    email = forms.EmailField(max_length=254)
    birth_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'alt', 'email', 'birth_date', 'password1', 'password2',)
        help_texts = {
            'first_name': 'Required',
            'last_name': 'Required',
            'alt': 'Optional. If given, this will replace your first and last name on your profile and in search',
            'email': 'Required. You will receive a validation email',
            'birth_date': 'Required. Format: YYYY-MM-DD. Users under 18 will not appear in search. You must be 13+ to sign up.'
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
        fields = ('image', 'alt', 'location', 'bio')
        help_texts = {
            'alt': 'If given, this will replace your first and last name on your profile and in search',
            'location': 'City name recommended',
        }
