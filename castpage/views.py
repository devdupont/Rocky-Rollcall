"""
View logic for cast page
"""

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
# Other apps
from notify.signals import notify
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
        'is_member': cast.is_member(request.user),
        'is_blocked': cast.is_blocked(request.user),
        'has_requested_membership': cast.has_requested_membership(request.user),
        'tinylist': True,
    })

@login_required
@cast_required
def request_to_join(request, cast: Cast):
    """
    Requests that the user join the cast
    """
    try:
        cast.add_member_request(request.user.profile)
        notify.send(request.user, recipient_list=cast.managers_as_user, actor=request.user,
                    verb='requested', target=cast, nf_type='cast_member_request')
        messages.success(request, f'A request has been sent to {cast} managers')
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect('cast_home', slug=cast.slug)

@login_required
@cast_required
def leave_cast(request, cast: Cast):
    """
    Remove the user from the cast
    """
    try:
        cast.remove_member(request.user.profile)
        messages.success(request, f'You have left {cast}')
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect('cast_home', slug=cast.slug)

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

    @property
    def requested_by_manager(self) -> bool:
        """
        Returns True if the page was requested by a cast manager
        """
        return self.cast.is_manager(self.request.user)

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        cast = self.cast
        context['cast'] = cast
        context['show_management'] = self.requested_by_manager
        return context

class CastMembers(CastBaseListView):
    """
    Pagination view for cast members
    """

    model = Profile
    template_name = 'castpage/members.html'
    paginate_by = 24
    context_object_name = 'profiles'

    def get_queryset(self) -> [Profile]:
        """
        Return all cast members
        """
        return sorted(self.cast.members.all(), key=lambda x: x.name.lower())

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        if context['show_management']:
            context['profile_buttons'] = 'castadmin/include/buttons/members.html'
        return context

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
