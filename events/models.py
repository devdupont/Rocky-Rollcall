"""
Models to manage calendar events
"""

# stdlib
from datetime import date, timedelta
# django
from django.db import models
from django.utils import timezone

EXPIRES_AFTER = 90 # days

class Event(models.Model):
    """
    A calendar event
    """

    name = models.CharField(max_length=128)
    description = models.TextField()
    venue = models.CharField(max_length=256)
    date = models.DateField()
    start_time = models.TimeField()

    cast = models.ForeignKey('castpage.Cast', on_delete=models.CASCADE, related_name='events')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date', 'start_time']

    @property
    def is_expired(self) -> bool:
        """
        Returns if an event is ready for deletion
        """
        return date.today() > self.date + timedelta(days=EXPIRES_AFTER)

    def __str__(self) -> str:
        return f"{self.cast.name} | {self.date} | {self.start_time}"

def get_upcoming_events(days: int = 14, limit: int = 12, cast: int = None) -> dict:
    """
    Returns upcoming events as a calendar dictionary
    """
    search = {
        'date__gte': date.today(),
        'date__lte': date.today()+timedelta(days=days),
    }
    if cast:
        search['cast__pk'] = cast
    # pylint: disable=E1101
    events = Event.objects.filter(**search)[:limit]
    calendar = {}
    for event in events:
        day = event.date
        if day in calendar:
            calendar[day].append(event)
        else:
            calendar[day] = [event]
    return calendar
