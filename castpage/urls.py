"""
Castpage URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('new', views.cast_new, name='cast_new'),
    path('<slug:slug>', views.cast_home, name='cast_home'),
    path('<slug:slug>/events', views.CastEvents.as_view(), name='cast_events'),
    path('<slug:slug>/admin/', views.cast_admin, name='cast_admin'),
    path('<slug:slug>/admin/section/new/', views.cast_section_new, name='cast_section_new'),
    path('<slug:slug>/admin/section/<int:pk>/edit/', views.cast_section_edit, name='cast_section_edit'),
    path('<slug:slug>/admin/section/<int:pk>/remove/', views.cast_section_remove, name='cast_section_remove'),
    path('<slug:slug>/admin/edit', views.cast_admin_edit, name='cast_admin_edit'),
    path('<slug:slug>/admin/managers', views.cast_admin_managers, name='cast_admin_managers'),
    path('<slug:slug>/admin/managers/delete/<int:pk>', views.cast_admin_managers_delete, name='cast_admin_managers_delete'),
]
