"""
Events URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('new/<slug:slug>', views.event_new, name='event_new'),
    path('edit/<int:pk>', views.event_edit, name='event_edit'),
    path('delete/<int:pk>', views.event_delete, name='event_delete'),
]
