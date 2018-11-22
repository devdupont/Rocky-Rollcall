"""
View logic for cast management
"""

# django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
# library
from notify.signals import notify
# app
from userprofile.models import Profile
from castadmin.forms import AddManagerForm, CastForm, CastPhotoForm, DeleteCastForm, PageSectionForm
from castpage.models import Cast, PageSection, Photo

def manager_required(func) -> 'Callable':
    """
    Decorator for views which require:
    1. An authenticated User
    2. An existing cast matching a slug
    3. The user is a manager of the cast
    """
    @login_required
    def managed_view(request, slug: str, *args, **kwargs):
        cast = get_object_or_404(Cast, slug=slug)
        if not cast.is_manager(request.user):
            return HttpResponseForbidden()
        return func(request, cast, *args, **kwargs)
    return managed_view

@manager_required
def cast_admin(request, cast: Cast):
    """
    Renders cast admin page
    """
    return render(request, 'castadmin/admin.html', {'cast': cast})

@manager_required
def cast_edit(request, cast: Cast):
    """
    Edit existing cast info
    """
    if request.method == 'POST':
        form = CastForm(request.POST, request.FILES, instance=cast)
        if form.is_valid():
            cast = form.save()
            messages.success(request, 'Cast info has been updated')
            return redirect('cast_admin', slug=cast.slug)
    else:
        form = CastForm(instance=cast)
    return render(request, 'castadmin/cast_edit.html', {
        'cast': cast,
        'form': form,
        'tinymce_api_key': settings.TINYMCE_API_KEY,
    })

@manager_required
def cast_delete(request, cast: Cast):
    """
    Delete a cast after verification
    """
    if cast.managers.count() > 1:
        messages.info(request, 'Other managers must be removed before you can delete a cast')
        return redirect('cast_admin', slug=cast.slug)
    if request.method == 'POST':
        form = DeleteCastForm(request.POST)
        if form.is_valid():
            castname = cast.name
            if form.cleaned_data.get('name') == castname:
                cast.delete()
                messages.success(request, f'You successfully deleted {castname}')
                return redirect('user_settings')
            else:
                messages.error(request, 'The cast name does not match')
    else:
        form = DeleteCastForm()
    return render(request, 'castadmin/delete.html', {
        'cast': cast,
        'form': form,
    })

@manager_required
def section_new(request, cast: Cast):
    """
    Add a new PageSection to a cast's home page
    """
    if request.method == 'POST':
        form = PageSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            messages.success(request, f'"{section.title}" has been created')
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm()
    return render(request, 'castadmin/section_edit.html', {
        'cast': cast,
        'form': form,
        'tinymce_api_key': settings.TINYMCE_API_KEY,
    })

@manager_required
def section_edit(request, cast: Cast, pk: int):
    """
    Edit an existing section of a cast's home page
    """
    section = get_object_or_404(PageSection, pk=pk)
    if request.method == 'POST':
        form = PageSectionForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            messages.success(request, f'"{section.title}" has been updated')
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm(instance=section)
    return render(request, 'castadmin/section_edit.html', {
        'cast': cast,
        'form': form,
        'tinymce_api_key': settings.TINYMCE_API_KEY,
    })

@manager_required
def section_delete(request, cast: Cast, pk: int):
    """
    Remove a section from a cast's home page
    """
    section = get_object_or_404(PageSection, pk=pk)
    section.delete()
    messages.success(request, f'"{section.title}" has been deleted')
    return redirect('cast_home', slug=cast.slug)

@manager_required
def photo_new(request, cast: Cast):
    """
    Add a new Photo to a cast
    """
    if request.method == 'POST':
        form = CastPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.cast = cast
            photo.save()
            messages.success(request, f'Photo has been added')
            return redirect('cast_photo_detail', slug=cast.slug, pk=photo.pk)
    else:
        form = CastPhotoForm()
    return render(request, 'castadmin/photo_edit.html', {
        'cast': cast,
        'form': form,
    })

@manager_required
def photo_edit(request, cast: Cast, pk: int):
    """
    Edit Photo information
    """
    photo = get_object_or_404(Photo, pk=pk)
    if cast != photo.cast:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CastPhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.cast = cast
            photo.save()
            messages.success(request, f'Photo has been updated')
            return redirect('cast_photo_detail', slug=cast.slug, pk=photo.pk)
    else:
        form = CastPhotoForm(instance=photo)
    return render(request, 'castadmin/photo_edit.html', {
        'cast': cast,
        'form': form,
    })

@manager_required
def photo_delete(request, cast: Cast, pk: int):
    """
    Delete a Photo from a cast
    """
    photo = get_object_or_404(Photo, pk=pk)
    if cast != photo.cast:
        return HttpResponseForbidden()
    photo.delete()
    messages.success(request, f'Photo has been deleted')
    return redirect('cast_home', slug=cast.slug)

@manager_required
def approve_request(request, cast: Cast, username: str):
    """
    Approves a cast membership request
    """
    user = get_object_or_404(User, username=username)
    try:
        cast.remove_member_request(user.profile)
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        try:
            cast.add_member(user.profile)
        except ValueError as exc:
            messages.error(request, str(exc))
        else:
            notify.send(request.user, recipient=user, actor=request.user,
                        verb='approved', obj=user, target=cast, nf_type='cast_member_result')
            messages.success(request, f'{user.profile.name} is now a member of {cast}')
    return redirect('cast_member_requests', slug=cast.slug)

@manager_required
def deny_request(request, cast: Cast, username: str):
    """
    Denies a cast membership request
    """
    user = get_object_or_404(User, username=username)
    try:
        cast.remove_member_request(user.profile)
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        notify.send(request.user, recipient=user, actor=request.user,
                    verb='denied', obj=user, target=cast, nf_type='cast_member_result')
        messages.success(request, f'Request from {user.profile.name} has been denied')
    return redirect('cast_member_requests', slug=cast.slug)

@manager_required
def block_user(request, cast: Cast, username: str):
    """
    Blocks a user from the cast
    """
    user = get_object_or_404(User, username=username)
    try:
        if cast.is_member(user):
            cast.remove_member(user.profile)
        elif cast.has_requested_membership(user):
            cast.remove_member_request(user.profile)
        cast.block_user(user.profile)
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        notify.send(request.user, recipient=user, actor=request.user,
                    verb='blocked', obj=user, target=cast, nf_type='cast_blocked')
        messages.success(request, f'{user.profile.name} has been blocked from {cast}')
    return redirect('cast_blocked_users', slug=cast.slug)

@manager_required
def unblock_user(request, cast: Cast, username: str):
    """
    Unblocks a user from the cast
    """
    user = get_object_or_404(User, username=username)
    try:
        cast.unblock_user(user.profile)
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        notify.send(request.user, recipient=user, actor=request.user,
                    verb='unblocked', obj=user, target=cast, nf_type='cast_blocked')
        messages.success(request, f'{user.profile.name} has been unblocked from {cast}')
    return redirect('cast_blocked_users', slug=cast.slug)

@manager_required
def managers_edit(request, cast: Cast):
    """
    Cast manager list and add page
    """
    if request.method == 'POST':
        form = AddManagerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            if user:
                user = user[0]
                try:
                    cast.add_manager(user.profile)
                except ValueError as exc:
                    messages.error(request, str(exc))
                else:
                    notify.send(request.user, recipient_list=cast.managers_as_user, actor=request.user,
                                verb='added', obj=user, target=cast, nf_type='cast_manager')
                    messages.success(request, f'{user.profile.name} has been added as a manager')
            else:
                messages.error(request, f'Could not find an account for "{username}"')
            return redirect('cast_managers_edit', slug=cast.slug)
    else:
        form = AddManagerForm()
    return render(request, 'castadmin/managers.html', {
        'cast': cast,
        'form': form,
    })

@manager_required
def managers_delete(request, cast: Cast, pk: int):
    """
    Remove a user from cast managers
    """
    user = get_object_or_404(User, pk=pk)
    if cast.managers.count() < 2:
        messages.error(request, 'Casts must have at least one manager')
    elif request.user == user:
        messages.error(request, 'You cannot remove yourself')
    else:
        try:
            cast.remove_manager(user.profile)
        except ValueError as exc:
            messages.error(request, str(exc))
        else:
            notify.send(request.user, recipient_list=cast.managers_as_user+[user], actor=request.user,
                        verb='removed', obj=user, target=cast, nf_type='cast_manager')
            messages.success(request, f'{user.username} is no longer a manager')
    return redirect('cast_managers_edit', slug=cast.slug)

class CastManagementListView(ListView):
    """
    Base class to provide manager-only list views
    """

    model = Profile
    paginate_by = 24
    context_object_name = 'profiles'
    profile_buttons = None

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
        context['cast'] = self.cast
        context['profile_buttons'] = self.profile_buttons
        return context

    def dispatch(self, request, *args, **kwargs):
        """
        Only allow managers to view the list
        """
        if not self.cast.is_manager(request.user):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

class MemberRequests(CastManagementListView):
    """
    Pagination view for cast membership requests
    """

    template_name = 'castadmin/member_requests.html'
    profile_buttons = 'castadmin/include/buttons/member_requests.html'

    def get_queryset(self) -> [Profile]:
        """
        Return all users requesting membership
        """
        return sorted(self.cast.member_requests.all(), key=lambda x: x.name.lower())

class BlockedUsers(CastManagementListView):
    """
    Pagination view for blocked users
    """

    template_name = 'castadmin/blocked_users.html'
    profile_buttons = 'castadmin/include/buttons/blocked_users.html'

    def get_queryset(self) -> [Profile]:
        """
        Return all blocked users
        """
        return sorted(self.cast.blocked.all(), key=lambda x: x.name.lower())
