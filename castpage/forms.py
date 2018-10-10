"""
Cast page form classes
"""

from django import forms
from .models import Cast, PageSection

class CastForm(forms.ModelForm):

    class Meta:
        model = Cast
        fields = (
            'name', 'description', 'logo',
            'external_url', 'facebook_url', 'twitter_user', 'instagram_user',
        )
        help_texts = {
            'external_url': 'Your existing website URL. Ex: https://mycast.com',
            'facebook_url': 'Public Facebook cast group URL. Ex: https://facebook.com/mycast',
            'twitter_user': 'Twitter @username. Ex: mycast',
            'instagram_user': 'Instagram @username. Ex: mycast',
        }

class PageSectionForm(forms.ModelForm):

    class Meta:
        model = PageSection
        fields = ('title', 'text',)

class AddManagerForm(forms.Form):

    username = forms.CharField(max_length=150)
