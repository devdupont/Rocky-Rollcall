"""
View logic for user management
"""

# django
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.contrib.auth.models import User
# app
from userprofile.models import Profile

def user_required(f) -> 'Callable':
    """
    Decorator to convert a slug to a user object
    """
    def profile_view(request, username: str, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        return f(request, user, *args, **kwargs)
    return profile_view

@user_required
def user_profile(request, user: User):
    """
    Renders user profile page
    """
    return render(request, 'userprofile/home.html', {
        'user': user,
    })
