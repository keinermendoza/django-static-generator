from django.urls import path
from . import views

urlpatterns = [
    path('<slug:project_slug>', views.free_view, name="free"),
    path('preview/<slug:project_slug>', views.preview_site_page, name="preview"),
    path('projects/<slug:project_slug>', views.list_site_pages, name="projects"),
]