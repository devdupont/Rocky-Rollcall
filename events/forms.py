"""
Event form classes
"""

# django
from django import forms
# library
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
# app
from events.models import Casting, Event

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

class CastingForm(forms.ModelForm):

    class Meta:
        model = Casting
        fields = ('role', 'profile', 'writein')

    def __init__(self, *args, **kwargs):
        cast = kwargs.pop('cast')
        super().__init__(*args, **kwargs)
        if cast:
            self.fields['profile'].queryset = cast.members.all()

    def clean(self):
        """
        Validates form fields

        Form must include a profile or write-in name to be valid
        """
        profile, writein = self.cleaned_data.get('profile'), self.cleaned_data.get('writein')
        if profile:
            self.cleaned_data['writein'] = ''
        elif writein:
            self.cleaned_data['profile'] = None
        else:
            msg = 'You must supply a cast member profile or a write-in name'
            self.add_error('profile', msg)
            self.add_error('writein', msg)
        return self.cleaned_data
