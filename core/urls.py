from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile_show, name="profile_show"),
]