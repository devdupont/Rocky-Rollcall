"""
Event form classes
"""

# django
from django import forms
# library
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
# app
from events.models import Event

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'venue', 'date', 'start_time', 'description',)
        help_texts = {
            'venue': 'This should map to a single location in Google Maps search',
            'start_time': "If it's a midnight show, you might want to set the start time at 11:59 PM to clarify the performance date",
        }
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'start_time': TimePickerInput(),
        }
