"""
Cast admin URL patterns
"""

from django.urls import path
from . import views

_s = '<slug:slug>/'

urlpatterns = [
    path(_s, views.cast_admin, name='cast_admin'),
    path(_s+'section/new/', views.section_new, name='cast_section_new'),
    path(_s+'section/<int:pk>/edit/', views.section_edit, name='cast_section_edit'),
    path(_s+'section/<int:pk>/remove/', views.section_delete, name='cast_section_delete'),
    path(_s+'edit', views.cast_edit, name='cast_edit'),
    path(_s+'managers', views.managers_edit, name='cast_managers_edit'),
    path(_s+'managers/delete/<int:pk>', views.managers_delete, name='cast_managers_delete'),
]
