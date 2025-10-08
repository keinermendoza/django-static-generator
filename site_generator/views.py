from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import TemplateGenerator 


def free_view(request):
    # search the template by slug
        # return 404 if not found

    default_project = TemplateGenerator.objects.first()
    
    # get buffer zip buffer
    zip_buffer = default_project.generate_zip_buffer()

    # return attached zip file
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")    
    response['Content-Disposition'] = 'attachment; filename="template_site.zip"'
    return response