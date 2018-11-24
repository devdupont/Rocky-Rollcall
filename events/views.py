"""
View logic for calendar event management
"""

# stdlib
from datetime import date
# django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
# app
from castpage.models import Cast
from events.forms import CastingForm, EventForm
from events.models import Casting, Event

def event_required(func) -> 'Callable':
    """
    Decorator to convert an int to an Event object
    """
    def event_view(request, pk: int, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        return func(request, event, *args, **kwargs)
    return event_view

@login_required
def event_new(request, slug: str):
    """
    Create a new event associated with a cast
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.cast = cast
            event.save()
            messages.success(request, f'"{event.name}" has been created')
            if 'more' not in request.POST:
                return redirect('cast_events', slug=cast.slug)
    else:
        form = EventForm()
    return render(request, 'events/event_edit.html', {
        'form': form,
        'form_title': 'New Event',
        'show_ca_button': True,
    })

@event_required
def event_detail(request, event: Event):
    """
    Renders the event detail page
    """
    form = None
    if event.cast.is_manager(request.user):
        if request.method == 'POST':
            form = CastingForm(request.POST, cast=None)
            if form.is_valid():
                casting = form.save(commit=False)
                casting.event = event
                casting.save()
                messages.success(request, f'Casting for {casting.role_tag} has been added')
                form = CastingForm(cast=event.cast)
        else:
            form = CastingForm(cast=event.cast)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'form': form,
    })

@login_required
@event_required
def event_edit(request, event: Event):
    """
    Edit an existing event by primary key
    """
    if not event.cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'"{event.name}" has been updated')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_edit.html', {
        'form': form,
        'form_title': 'Edit Event',
    })

@login_required
@event_required
def event_delete(request, event: Event):
    """
    Delete an existing event by primary key
    """
    if not event.cast.is_manager(request.user):
        return HttpResponseForbidden()
    event_name = event.name
    slug = event.cast.slug
    event.delete()
    messages.success(request, f'"{event_name}" has been deleted')
    return redirect('cast_home', slug=slug)

@login_required
def casting_delete(request, pk: int):
    """
    Deletes an existing casting by primary key
    """
    casting = get_object_or_404(Casting, pk=pk)
    if not casting.event.cast.is_manager(request.user):
        return HttpResponseForbidden()
    event_pk = casting.event.pk
    casting.delete()
    return redirect('event_detail', pk=event_pk)

class EventListView(ListView):
    """
    Pagination view for future events
    """

    model = Event
    paginate_by = 12
    context_object_name = 'events'
    queryset = Event.objects.filter(date__gte=date.today())

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        context['show_cast'] = True
        return context
