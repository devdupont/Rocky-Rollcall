from datetime import date
from django.shortcuts import render
from castpage.models import Cast
from events.models import Event

def home(request):
    """
    Renders the landing page
    """
    # pylint: disable=E1101
    return render(request, 'landingpage/landingpage.html', {
        'casts': Cast.objects.all(),
        'events': Event.objects.filter(date__gte=date.today())[:3],
        'show_cast': True,
        'tinylist': True,
    })
