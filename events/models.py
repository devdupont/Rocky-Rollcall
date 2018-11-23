"""
Models to manage calendar events
"""

# stdlib
from datetime import date, timedelta
# django
from django.db import models
from django.utils import timezone
from django_enumfield import enum

EXPIRES_AFTER = 90 # days

class Event(models.Model):
    """
    A calendar event
    """

    name = models.CharField(max_length=128, verbose_name='Event Name')
    description = models.TextField()
    venue = models.CharField(max_length=256)
    date = models.DateField()
    start_time = models.TimeField(verbose_name='Start Time')

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
    events = Event.objects.filter(**search)[:limit]
    calendar = {}
    for event in events:
        day = event.date
        if day in calendar:
            calendar[day].append(event)
        else:
            calendar[day] = [event]
    return calendar

class Role(enum.Enum):
    """
    Roles performed at an event
    """

    FRANK = 1
    JANET = 2
    BRAD = 3
    RIFF = 4
    MAGENTA = 5
    COLUMBIA = 6
    SCOTT = 7
    ROCKY = 8
    EDDIE = 9
    CRIM = 10
    TRANSY = 11

    EMCEE = 20
    TRIXIE = 21

    TECH = 30
    LIGHTS = 31
    PHOTOS = 32

    labels = {
        FRANK: 'Dr. Frank-N-Furter',
        JANET: 'Janet Weiss',
        BRAD: 'Brad Majors',
        RIFF: 'Riff Raff',
        MAGENTA: 'Magenta',
        COLUMBIA: 'Columbia',
        SCOTT: 'Dr. Everett V. Scott',
        ROCKY: 'Rocky Horror',
        EDDIE: 'Eddie',
        CRIM: 'The Criminologist',
        TRANSY: 'Transylvanian',

        EMCEE: 'Emcee',
        TRIXIE: 'Trixie',

        TECH: 'Tech',
        LIGHTS: 'Lights',
        PHOTOS: 'Photographer',
    }

class Casting(models.Model):
    """
    Represents a User being cast in a Role at an Event
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='castings')
    profile = models.ForeignKey('userprofile.Profile', on_delete=models.CASCADE, related_name='castings')
    role = enum.EnumField(Role)

    class Meta:
        ordering = ['role']

    @property
    def role_tag(self) -> Role:
        """
        Returns the role as the Role enum
        """
        return Role.get(self.role)

    @property
    def show_picture(self) -> bool:
        """
        Returns True if the casting is a non-tech role
        """
        return self.role < 30
