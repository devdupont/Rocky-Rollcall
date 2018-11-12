"""
View logic for user management
"""

# django
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# app
from photos.views import PhotoGridView
from useradmin.forms import UserPhotoForm
from userprofile.models import Photo, Profile

def user_required(f) -> 'Callable':
    """
    Decorator to convert a username to a user object
    """
    def profile_view(request, username: str, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        return f(request, user, *args, **kwargs)
    return profile_view

def is_user(f) -> 'Callable':
    """
    Decorator to verify profile belongs to request.user
    """
    @login_required
    def profile_auth_view(request, username: str, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        if user != request.user:
            return HttpResponseForbidden()
        return f(request, *args, **kwargs)
    return profile_auth_view

@user_required
def user_profile(request, user: User):
    """
    Renders user profile page
    """
    return render(request, 'userprofile/home.html', {
        'user': user,
    })

@user_required
def photo_detail(request, user: User, pk: int):
    """
    Renders a photo detail page
    """
    photo = user.profile.photos.filter(pk=pk)
    if not photo:
        return HttpResponseNotFound()
    return render(request, 'userprofile/photo_detail.html', {
        'user': user,
        'photo': photo[0],
    })

@is_user
def photo_new(request):
    """
    Add a new Photo to a user profile
    """
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.profile = request.user.profile
            photo.save()
            messages.success(request, f'Photo has been added')
            return redirect('user_photo_detail', username=request.user.username, pk=photo.pk)
    else:
        form = UserPhotoForm()
    return render(request, 'userprofile/photo_edit.html', {
        'form': form,
    })

@is_user
def photo_edit(request, pk: int):
    """
    Edit Photo information
    """
    photo = get_object_or_404(Photo, pk=pk)
    if photo.profile.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.profile = request.user.profile
            photo.save()
            messages.success(request, f'Photo has been updated')
            return redirect('user_photo_detail', username=request.user.username, pk=photo.pk)
    else:
        form = UserPhotoForm(instance=photo)
    return render(request, 'useradmin/photo_edit.html', {
        'form': form,
    })

@is_user
def photo_delete(request, pk: int):
    """
    Delete a Photo from a user
    """
    photo = get_object_or_404(Photo, pk=pk)
    if photo.profile.user != request.user:
        return HttpResponseForbidden()
    photo.delete()
    messages.success(request, f'Photo has been deleted')
    return redirect('user_settings')

class UserPhotos(PhotoGridView):
    """
    Pagination view for cast photos
    """

    model = Photo
    template_name = 'userprofile/photos.html'

    def get_queryset(self) -> [Photo]:
        """
        Filter queryset to user photos
        """
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.profile.photos.all()

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['user'] = user
        return context
