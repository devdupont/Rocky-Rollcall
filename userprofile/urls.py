"""
User URL patterns
"""

from django.urls import path
from userprofile import views

_s = '<slug:username>/'

urlpatterns = [
    path(_s, views.user_profile, name='user_profile'),
    path(_s+'photos', views.UserPhotos.as_view(), name='user_photos'),
    path(_s+'photos/new', views.photo_new, name='user_photo_new'),
    path(_s+'photos/<int:pk>', views.photo_detail, name='user_photo_detail'),
    path(_s+'photos/<int:pk>/edit', views.photo_edit, name='user_photo_edit'),
    path(_s+'photos/<int:pk>/delete', views.photo_delete, name='user_photo_delete'),
]
