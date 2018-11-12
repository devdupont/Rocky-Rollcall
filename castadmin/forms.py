"""
Cast admin form classes
"""

from django import forms
from photos.forms import PhotoForm
from castpage.models import Cast, PageSection, Photo

class CastForm(forms.ModelForm):

    class Meta:
        model = Cast
        fields = (
            'name', 'logo', 'email',
            'external_url', 'facebook_url', 'twitter_user', 'instagram_user',
            'description',
        )
        help_texts = {
            'name': 'Cast name (including URL name) must be unique',
            'logo': 'Cast logos will be centered and cropped into squares',
            'email': 'Email for questions about attending and booking shows',
            'external_url': 'Your existing website URL. Ex: https://mycast.com',
            'facebook_url': 'Public Facebook cast group URL. Ex: https://facebook.com/mycast',
            'twitter_user': 'Twitter @username. Ex: mycast',
            'instagram_user': 'Instagram @username. Ex: mycast',
        }

class DeleteCastForm(forms.Form):

    name = forms.CharField(max_length=128, help_text='Type the cast name to confirm deletion')

class PageSectionForm(forms.ModelForm):

    class Meta:
        model = PageSection
        fields = ('title', 'order', 'text',)

class CastPhotoForm(PhotoForm):

    class Meta(PhotoForm.Meta):
        model = Photo

class AddManagerForm(forms.Form):

    username = forms.CharField(max_length=150)
