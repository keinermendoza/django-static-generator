from django.apps import AppConfig
from django.core.signals import request_finished

class SiteGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_generator'

    def ready(self):
        from . import signals
