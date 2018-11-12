from django import forms

class PhotoForm(forms.ModelForm):

    class Meta:
        fields = ('image', 'description')
