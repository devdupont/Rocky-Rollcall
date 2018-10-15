"""
Cast admin URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.cast_admin, name='cast_admin'),
    path('<slug:slug>/section/new/', views.section_new, name='cast_section_new'),
    path('<slug:slug>/section/<int:pk>/edit/', views.section_edit, name='cast_section_edit'),
    path('<slug:slug>/section/<int:pk>/remove/', views.section_delete, name='cast_section_delete'),
    path('<slug:slug>/edit', views.cast_edit, name='cast_edit'),
    path('<slug:slug>/managers', views.managers_edit, name='cast_managers_edit'),
    path('<slug:slug>/managers/delete/<int:pk>', views.managers_delete, name='cast_managers_delete'),
]
