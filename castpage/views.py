"""
View logic for cast page and management
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from events.views import EventListView
from .forms import CastForm, PageSectionForm
from .models import Cast, PageSection

@login_required
def cast_new(request):
    """
    Create a new cast
    """
    if request.method == 'POST':
        form = CastForm(request.POST, request.FILES)
        if form.is_valid():
            cast = form.save()
            cast.managers.add(request.user.profile)
            cast.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = CastForm()
    return render(request, 'castpage/cast_edit.html', {'form': form})

def cast_home(request, slug: str):
    """
    Renders the cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    return render(request, 'castpage/home.html', {
        'cast': cast,
        'show_management': cast.is_manager(request.user)
    })

class CastEvents(EventListView):
    """
    Pagination view for future cast events
    """

    template_name = 'castpage/event_list.html'
    paginate_by=2

    def get_queryset(self) -> ['Event']:
        """
        Filter queryset based on cast events
        """
        cast = get_object_or_404(Cast, slug=self.kwargs['slug'])
        return cast.future_events

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        context['cast'] = get_object_or_404(Cast, slug=self.kwargs['slug'])
        return context

@login_required
def cast_section_new(request, slug: str):
    """
    Add a new PageSection to a cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PageSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm()
    return render(request, 'castpage/section_edit.html', {'cast': cast, 'form': form})

@login_required
def cast_section_edit(request, slug: str, pk: int):
    """
    Edit an existing section of a cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    section = get_object_or_404(PageSection, pk=pk)
    if request.method == 'POST':
        form = PageSectionForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm(instance=section)
    return render(request, 'castpage/section_edit.html', {'cast': cast, 'form': form})

@login_required
def cast_section_remove(request, slug: str, pk: int):
    """
    Remove a section from a cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    section = get_object_or_404(PageSection, pk=pk)
    section.delete()
    return redirect('cast_home', slug=cast.slug)

@login_required
def cast_admin(request, slug: str):
    """
    Renders cast admin page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    return render(request, 'castpage/admin.html', {'cast': cast})

@login_required
def cast_admin_edit(request, slug: str):
    """
    Edit existing cast info
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CastForm(request.POST, request.FILES, instance=cast)
        if form.is_valid():
            cast = form.save()
            messages.success(request, 'Cast info has been updated')
            return redirect('cast_admin', slug=cast.slug)
    else:
        form = CastForm(instance=cast)
    return render(request, 'castpage/cast_edit.html', {
        'cast': cast,
        'form': form,
    })
