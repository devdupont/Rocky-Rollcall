"""
User URL patterns
"""

from django.urls import path
from userprofile import views

_s = '<slug:username>/'

urlpatterns = [
    path(_s, views.user_profile, name='user_profile'),

]
