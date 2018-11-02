"""
Search URL patterns
"""

from django.urls import path
from . import views

urlpatterns = [
    path('casts', views.CastSearchListView.as_view(), name='cast_search'),
]
