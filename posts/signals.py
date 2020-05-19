from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Post


@receiver(pre_save, sender=Post)
def get_publish_date(sender, instance, *args, **kwargs):
    if instance.active and not instance.published:
        instance.published = timezone.now()
    if not instance.active and instance.published:
        instance.published = None
