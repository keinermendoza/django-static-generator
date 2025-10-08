from django.shortcuts import render
from site_generator.models import TemplateGenerator

def home(request):
    template_name = "shop/project/list.html"
    project_templates = TemplateGenerator.objects.all()
    return render(request, template_name, {"project_templates":project_templates})

