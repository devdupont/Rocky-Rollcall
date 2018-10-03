"""
Castpage URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('new', views.cast_new, name='cast_new'),
    path('<slug:slug>', views.cast_home, name='cast_home'),
    path('<slug:slug>/section/new/', views.cast_section_new, name='cast_section_new'),
    path('<slug:slug>/section/<int:pk>/edit/', views.cast_section_edit, name='cast_section_edit'),
    path('<slug:slug>/section/<int:pk>/remove/', views.cast_section_remove, name='cast_section_remove'),
]
