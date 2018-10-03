from django.shortcuts import render
from castpage.models import Cast

def home(request):
    """
    Renders the landing page
    """
    # pylint: disable=E1101
    return render(request, 'landingpage/landingpage.html', {
        'casts': Cast.objects.all()
    })
