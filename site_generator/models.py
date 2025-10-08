from config import settings
from django.db import models
from io import BytesIO
import zipfile
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders

class TemplateGenerator(models.Model):
    project_name = models.CharField(max_length=80)
    template_names = models.JSONField(default=list)
    css_files = models.JSONField(default=list)
    js_files = models.JSONField(default=list)

    def get_template_string(self, template_name, context={}):
        template_path = settings.BASE_DIR / "templates" / "generator" / self.project_name  / template_name 
        return render_to_string(template_path, context)
    
    def get_css_path(self, filename):
        return settings.BASE_DIR / "static" / "generator" / self.project_name  / "css" / filename 

    def get_js_path(self, filename):
        return settings.BASE_DIR / "static" / "generator" / self.project_name  / "js" / filename

    def generate_zip_buffer(self, context={}):
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