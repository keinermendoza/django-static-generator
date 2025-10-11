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
    page_filename = request.GET.get("page-filename")
    if not page_filename:
        page_filename =  "index.html"

    print("saindo...", page_filename)
    context = {
        "title" : request.GET.get("title"),
        "demo_mode": True,
        "project": project,
        "page_filename": page_filename
    }
    
    if page_filename in project.template_names:
        return render(request, project.get_template_path(page_filename), context) 
    return HttpResponse(404)