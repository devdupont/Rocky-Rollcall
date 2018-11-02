"""
Search form classes
"""

# django
from django import forms

class CastSearchForm(forms.Form):

    name = forms.CharField(max_length=128, label='Cast Name')
