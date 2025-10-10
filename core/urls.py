from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile_show, name="profile_show"),
    path('profile/edit', views.profile_edit, name="profile_edit"),
]