from django.contrib import admin
from django import forms
from .models import TemplateGenerator, TemplateRanked
@admin.register(TemplateGenerator)
class TemplateGeneratorAdmin(admin.ModelAdmin):
    list_display = ['project_name']

    prepopulated_fields = {
        'slug': ('project_name',)
    }

admin.site.register(TemplateRanked)