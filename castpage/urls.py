from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.cast_home, name='cast_home'),
]
