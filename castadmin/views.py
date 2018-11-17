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
# library
from notify.signals import notify
# app
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
        cast.add_member(user.profile)
        notify.send(request.user, recipient=user, actor=request.user,
                    verb='approved', obj=user, target=cast, nf_type='cast_member_result')
        messages.success(request, f'{user.profile.name} is now a member of {cast}')
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect('cast_members', slug=cast.slug)

@manager_required
def deny_request(request, cast: Cast, username: str):
    """
    Denies a cast membership request
    """
    user = get_object_or_404(User, username=username)
    try:
        cast.remove_member_request(user.profile)
        notify.send(request.user, recipient=user, actor=request.user,
                    verb='denied', obj=user, target=cast, nf_type='cast_member_result')
        messages.success(request, f'Request from {user} has been denied')
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect('cast_members', slug=cast.slug)

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
                    notify.send(request.user, recipient_list=cast.managers_as_user, actor=request.user,
                                verb='added', obj=user, target=cast, nf_type='cast_manager')
                    messages.success(request, f'{user.profile.name} has been added as a manager')
                except ValueError as exc:
                    messages.error(request, str(exc))
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
        notify.send(request.user, recipient_list=cast.managers_as_user, actor=request.user,
                    verb='removed', obj=user, target=cast, nf_type='cast_manager')
        try:
            cast.remove_manager(user.profile)
            messages.success(request, f'{user.username} is no longer a manager')
        except ValueError as exc:
            messages.error(request, str(exc))
    return redirect('cast_managers_edit', slug=cast.slug)
