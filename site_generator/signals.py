from django.db.models.signals import post_save
from django.dispatch import receiver
from site_generator.models import TemplateRanked, TemplateGenerator

@receiver(post_save, sender=TemplateGenerator)
def create_template_ranked(sender,  instance, created, **kwargs):
    if created:
        TemplateRanked.objects.create(project=instance)