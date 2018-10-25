"""
View logic for user profiles and management
"""

from os import environ
from decouple import config

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import DeleteUserForm, EditUserForm, SignUpForm
from .tokens import account_activation_token

@login_required
def settings(request):
    """
    Renders user settings page
    """
    return render(request, 'userprofile/settings.html')

ACTIVATE_SUBJECT = 'Activate Your Rocky Rollcall Account'

def signup(request):
    """
    Create and validate a new user
    """
    if config('DISABLE_SIGNUP', default=False, cast=bool):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create a new, inactive user from form data
            user = form.save(commit=False)
            user.is_activate = False
            user.save()
            # Reload user after profile has been created
            user.refresh_from_db()
            user.profile.save_from_form(form)
            user.save()
            # Send user activation email
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'pk': user.pk,
                'token': account_activation_token.make_token(user),
            })
            user.email_user(ACTIVATE_SUBJECT, message)
            return redirect('user_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, pk, token):
    """
    Activates user from validation link or renders invalid page
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist: #pylint: disable=E1101
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.profile.save()
        user.save()
        login(request, user)
        return redirect('user_settings')
    else:
        return render(request, 'registration/activation_invalid.html')

def activation_sent(request):
    """
    Renders activation email sent page
    """
    return render(request, 'registration/activation_sent.html')

@login_required
def edit_user(request):
    """
    Edit a subset of auth.User fields
    """
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect('user_settings')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'registration/edit.html', {'form': form})

@login_required
def delete(request):
    """
    Delete a user account after verification
    """
    user = request.user
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('username') == user.username:
                logout(request)
                user.delete()
                messages.success(request, 'You successfully deleted your account')
                return redirect('landing_page')
            else:
                messages.error(request, 'Your username does not match')
    else:
        form = DeleteUserForm()
    return render(request, 'registration/delete.html', {'form': form})
