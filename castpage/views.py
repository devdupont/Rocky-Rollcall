"""
View logic for cast page
"""

# Django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
# Other apps
from castadmin.forms import CastForm
from events.views import EventListView
from photos.views import PhotoGridView
from userprofile.models import Profile
# This app
from castpage.models import Cast, Photo

def cast_required(func) -> 'Callable':
    """
    Decorator to convert a slug to a cast object
    """
    def cast_view(request, slug: str, *args, **kwargs):
        cast = get_object_or_404(Cast, slug=slug)
        return func(request, cast, *args, **kwargs)
    return cast_view

@login_required
def cast_new(request):
    """
    Create a new cast
    """
    if request.method == 'POST':
        form = CastForm(request.POST, request.FILES)
        if form.is_valid():
            cast = form.save()
            cast.members.add(request.user.profile)
            cast.managers.add(request.user.profile)
            cast.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = CastForm()
    return render(request, 'castadmin/cast_edit.html', {
        'form': form,
        'tinymce_api_key': settings.TINYMCE_API_KEY,
    })

@cast_required
def cast_home(request, cast: Cast):
    """
    Renders the cast's home page
    """
    return render(request, 'castpage/home.html', {
        'cast': cast,
        'show_management': cast.is_manager(request.user),
        'tinylist': True,
    })

@cast_required
def cast_photo_detail(request, cast: Cast, pk: int):
    """
    Renders a photo detail page
    """
    photo = cast.photos.filter(pk=pk)
    if not photo:
        return HttpResponseNotFound()
    return render(request, 'castpage/photo_detail.html', {
        'cast': cast,
        'photo': photo[0],
        'show_management': cast.is_manager(request.user),
    })

class CastBaseListView(ListView):
    """
    Pagination view for cast entities
    """

    @property
    def cast(self) -> Cast:
        """
        The current cast to query
        """
        cast = get_object_or_404(Cast, slug=self.kwargs['slug'])
        return cast

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        cast = self.cast
        context['cast'] = cast
        context['show_management'] = cast.is_manager(self.request.user)
        return context

class CastMembers(CastBaseListView):
    """
    Pagination view for cast members
    """

    model = Profile
    template_name = 'castpage/members.html'
    paginate_by = 24
    context_object_name = 'members'

    def get_queryset(self) -> [Profile]:
        """
        Return all cast members
        """
        return self.cast.members.all()

class CastEvents(EventListView, CastBaseListView):
    """
    Pagination view for future cast events
    """

    template_name = 'castpage/event_list.html'
    paginate_by = 12

    def get_queryset(self) -> ['Event']:
        """
        Return future cast events
        """
        return self.cast.future_events

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        context['show_cast'] = False
        return context

class CastPhotos(PhotoGridView, CastBaseListView):
    """
    Pagination view for cast photos
    """

    model = Photo
    template_name = 'castpage/photos.html'

    def get_queryset(self) -> [Photo]:
        """
        Return all cast photos
        """
        return self.cast.photos.all()
