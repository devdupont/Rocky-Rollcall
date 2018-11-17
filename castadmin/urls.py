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
    path(_s+'photo/new/', views.photo_new, name='cast_photo_new'),
    path(_s+'photo/<int:pk>/edit/', views.photo_edit, name='cast_photo_edit'),
    path(_s+'photo/<int:pk>/remove/', views.photo_delete, name='cast_photo_delete'),
    path(_s+'edit', views.cast_edit, name='cast_edit'),
    path(_s+'delete', views.cast_delete, name='cast_delete'),
    path(_s+'users/blocked', views.BlockedUsers.as_view(), name='cast_blocked_users'),
    path(_s+'users/blocked/<slug:username>/block', views.block_user, name='cast_block_user'),
    path(_s+'users/blocked/<slug:username>/unblock', views.unblock_user, name='cast_unblock_user'),
    path(_s+'users/requests', views.MemberRequests.as_view(), name='cast_member_requests'),
    path(_s+'users/requests/<slug:username>/approve', views.approve_request, name='cast_member_requests_approve'),
    path(_s+'users/requests/<slug:username>/deny', views.deny_request, name='cast_member_requests_deny'),
    path(_s+'users/managers', views.managers_edit, name='cast_managers_edit'),
    path(_s+'users/managers/delete/<int:pk>', views.managers_delete, name='cast_managers_delete'),
]
