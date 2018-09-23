"""
Cast page form classes
"""

from django import forms
from .models import PageSection

class PageSectionForm(forms.ModelForm):

    class Meta:
        model = PageSection
        fields = ('title', 'text',)