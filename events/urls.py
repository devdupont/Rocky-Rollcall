"""
Events URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('new/<slug:slug>', views.event_new, name='event_new'),
    path('<int:pk>', views.event_detail, name='event_detail'),
    path('<int:pk>/edit', views.event_edit, name='event_edit'),
    path('<int:pk>/delete', views.event_delete, name='event_delete'),
    path('casting/<int:pk>/delete', views.casting_delete, name='casting_delete'),
]
