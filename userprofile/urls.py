"""
User URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('settings', views.user_settings, name='user_settings'),
    path('signup', views.signup, name='user_signup'),
    path('activation_sent', views.activation_sent, name='user_activation_sent'),
    path('activate/<int:pk>/<slug:token>', views.activate, name='user_activate'),
    path('edit', views.edit_user, name='user_edit'),
    path('delete', views.delete, name='user_delete'),
    path('notifications', views.notifications, name='user_notifications'),
]
