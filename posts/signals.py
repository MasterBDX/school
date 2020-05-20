from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Post
from .utils import unique_slug_generator


@receiver(pre_save, sender=Post)
def get_publish_date(sender, instance, *args, **kwargs):
    if instance.active and not instance.published_date:
        instance.published_date = timezone.now()
    if not instance.active and instance.published_date:
        instance.published_date = None

    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
