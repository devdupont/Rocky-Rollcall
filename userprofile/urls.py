"""
User URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('settings', views.settings, name='user_settings'),
    path('signup', views.signup, name='signup'),
    path('activation_sent', views.activation_sent, name='activation_sent'),
    path('activate/<int:pk>/<slug:token>', views.activate, name='activate'),
]
