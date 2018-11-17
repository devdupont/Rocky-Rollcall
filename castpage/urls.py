"""
Castpage URL patterns
"""

from django.urls import path
from castpage import views

_s = '<slug:slug>/'

urlpatterns = [
    path('new', views.cast_new, name='cast_new'),
    path('<slug:slug>', views.cast_home, name='cast_home'),
    path(_s+'events', views.CastEvents.as_view(), name='cast_events'),
    path(_s+'members', views.CastMembers.as_view(), name='cast_members'),
    path(_s+'members/join', views.request_to_join, name='cast_member_join'),
    path(_s+'members/leave', views.leave_cast, name='cast_member_leave'),
    path(_s+'photos', views.CastPhotos.as_view(), name='cast_photos'),
    path(_s+'photos/<int:pk>', views.cast_photo_detail, name='cast_photo_detail'),
]
