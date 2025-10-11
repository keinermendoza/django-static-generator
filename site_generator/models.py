from config import settings
from django.db import models
from io import BytesIO
import zipfile
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.core.files.storage import default_storage
from django.urls import reverse

class TemplateGenerator(models.Model):
    project_name = models.CharField(max_length=80)
    template_names = models.JSONField(default=list)
    css_files = models.JSONField(default=list)
    js_files = models.JSONField(default=list)

    preview_image = models.ImageField(upload_to='projects/preview', blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=80, unique=True)

    PATH_TO_DEFAULT_IMAGE = "projects/preview/default.png"

    def get_template_path(self, template_name):
        return settings.BASE_DIR / "templates" / "generator" / self.project_name  / template_name 

    def get_template_string(self, template_name, context={}):
        return render_to_string(self.get_template_path(template_name), context)
    
    def get_css_path(self, filename):
        return settings.BASE_DIR / "static" / "generator" / self.project_name  / "css" / filename 

    def get_js_path(self, filename):
        return settings.BASE_DIR / "static" / "generator" / self.project_name  / "js" / filename

    def generate_zip_buffer(self, context=None):
        if context is None:
            context = {"project":self}
        
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip:
            # add templates
            for template in self.template_names:
                zip.writestr(template, self.get_template_string(template, context))

            # add css
            for css_filename in self.css_files:
                if path := finders.find(self.get_css_path(css_filename)):
                    with open(path, 'rb') as f:
                        content = f.read()
                        zip.writestr("css/" + css_filename, content)

            # add js
            for js_filename in self.js_files:
                if path := finders.find(self.get_js_path(js_filename)):
                    with open(path, 'rb') as f:
                        content = f.read()
                        zip.writestr("js/" + js_filename, content)

        zip_buffer.seek(0)
        return zip_buffer
    
    def __str__(self):
        return self.project_name
    
    def get_absolute_url(self):
        return reverse('projects', args=[self.slug])
    
    @property
    def image(self):
        if self.preview_image:
            return self.preview_image.url
        return default_storage.url(self.PATH_TO_DEFAULT_IMAGE)
    
class TemplateRanked(models.Model):
    project = models.OneToOneField(TemplateGenerator, related_name="ranking", on_delete=models.CASCADE)
    downloads = models.IntegerField(default=0)

    def up_downloads_count(self):
        self.downloads += 1
        self.save()

    def __str__(self):
        return f"{self.project} has {self.downloads} downloads"
