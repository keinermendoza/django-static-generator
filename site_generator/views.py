from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import TemplateGenerator 

def free_view(request, project_slug):
    project = get_object_or_404(TemplateGenerator, slug=project_slug)
    
    # get buffer zip buffer
    zip_buffer = project.generate_zip_buffer()

    # return attached zip file
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")    
    response['Content-Disposition'] = 'attachment; filename="template_site.zip"'
    return response

def list_site_pages(request, project_slug):
    project = get_object_or_404(TemplateGenerator, slug=project_slug)
    return render(request, "shop/project/detail.html", {"project": project})

def preview_site_page(request, project_slug):
    project = get_object_or_404(TemplateGenerator, slug=project_slug)
    filename = request.GET.get("page-filename")
    context = {
        "title" : request.GET.get("title")
    }
    
    if filename in project.template_names:
        return render(request, project.get_template_path(filename), context) 
    return HttpResponse(404)