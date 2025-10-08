from django.urls import path
from . import views

urlpatterns = [
    path('', views.free_view, name="free"),
    path('preview', views.preview_site_page, name="preview"),
    path('projects', views.list_site_pages, name="projects"),
]