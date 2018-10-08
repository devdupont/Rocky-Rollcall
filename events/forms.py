"""
Event form classes
"""

from django import forms
from .models import Event

class EventForm(forms.ModelForm):

    date = forms.DateField(
        help_text='Required. Format: YYYY-MM-DD',
        widget=forms.DateInput(attrs={'class':'datepicker'})
    )
    start_time = forms.TimeField(
        help_text='Required. Format: HH:MM:SS',
        widget=forms.TimeInput(attrs={'class':'timepicker'})
    )

    class Meta:
        model = Event
        fields = ('name', 'description', 'venue', 'date', 'start_time')
