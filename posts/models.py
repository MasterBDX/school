from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.urls import reverse
from .utils import unique_slug_generator
from django_resized import ResizedImageField

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_posts')
    overview = models.TextField()

    content = models.TextField(blank=True, null=True)
    main_image = ResizedImageField(size=[600, 350], blank=True, null=True)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [('author', 'Can add post')]
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def safe_content(self):
        return mark_safe(self.content)


def get_post_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(get_post_slug_receiver, sender=Post)
