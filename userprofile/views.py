"""
View logic for user profiles and management
"""

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token

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
            return redirect('activation_sent')
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
