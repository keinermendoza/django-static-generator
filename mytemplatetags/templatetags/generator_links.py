from django import template
from django.urls import reverse_lazy
from django.templatetags.static import static
from site_generator.models import TemplateGenerator
register = template.Library()

@register.simple_tag(takes_context=True)
def generator_link(context, asset, type: str):
    """
    Generates the correct URL for a project resource, depending on whether demo_mode is active.

    Args:
        context (dict): The template context, must include 'project' and may contain 'demo_mode'.
        asset (str): The resource file name.
        type (str): Resource type, must be 'html', 'css', or 'js'.

    Returns:
        str: Generated URL for the given resource.

    Raises:
        template.TemplateSyntaxError: If the type is invalid or project is not a TemplateGenerator instance.
    """
    if type not in ["html", "css", "js"]:
        raise template.TemplateSyntaxError(
            "tag 'generator_link' must by of type 'html' | 'css' | 'js'."
        )
    
    project = context.get("project", None)
    if not isinstance(project, TemplateGenerator):
        raise template.TemplateSyntaxError(
            "Tag 'generator_link' must receive a valid 'project' instance as part of its parent context."
        )
    
    link = '' 

    if context.get("demo_mode", False):
        match type:
            case 'html':
                link =  reverse_lazy('preview', args=[project.slug]) + '?page-filename=' + asset
            case 'css' | 'js':
                link = static(f"generator/{project.project_name}/{type}/{asset}")
    else:
        match type:
            case 'html':
                link =  "/" + asset
            case 'css' | 'js':
                link = f"./{type}/{asset}"
        
    return link