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
from .models import Profile

class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, help_text='Required')
    last_name = forms.CharField(max_length=30, help_text='Required')
    email = forms.EmailField(max_length=254, help_text='Required. You will receive a validation email')
    birth_date = forms.DateField(
        help_text='Required. Format: YYYY-MM-DD',
        widget=DatePickerInput(format='%Y-%m-%d')
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2',)

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class DeleteUserForm(forms.Form):

    username = forms.CharField(max_length=150, help_text='Type your username to confirm deletion')

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'location')
