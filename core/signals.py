from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser, UserAction

@receiver(post_save, sender=CustomUser)
def create_user_actions(sender,  instance, created, **kwargs):
    if created:
        UserAction.objects.create(user=instance)