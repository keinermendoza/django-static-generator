from django.contrib import admin
from .models import TemplateGenerator

@admin.register(TemplateGenerator)
class TemplateGeneratorAdmin(admin.ModelAdmin):
    list_display = ['project_name']

    prepopulated_fields = {
        'slug': ('project_name',)
    }