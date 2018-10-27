"""
Event form classes
"""

# django
from django import forms
# library
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
# app
from .models import Event

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'venue', 'date', 'start_time', 'description',)
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'start_time': TimePickerInput(),
        }
