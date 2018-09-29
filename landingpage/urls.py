"""
Landing page URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing_page'),
    path('signup', views.signup, name='signup'),
]
