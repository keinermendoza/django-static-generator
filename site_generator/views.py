from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import TemplateGenerator 


def free_view(request):
    # search site by slug
        # return 404 if not found

    default_project = TemplateGenerator.objects.first()
    
    # get buffer zip buffer
    zip_buffer = default_project.generate_zip_buffer()

    # return attached zip file
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")    
    response['Content-Disposition'] = 'attachment; filename="template_site.zip"'
    return response

def list_site_pages(request):
    # search site by slug
        # return 404 if not found

    default_project = TemplateGenerator.objects.first()
    return render(request, "shop/project.html", {"project": default_project})

def preview_site_page(request):
    # search site by slug
        # return 404 if not found

    default_project = TemplateGenerator.objects.first()
    filename = request.GET.get("page-filename")
    context = {
        "title" : request.GET.get("title")
    }
    
    if filename in default_project.template_names:
        return render(request, default_project.get_template_path(filename), context) 
    return HttpResponse(404)