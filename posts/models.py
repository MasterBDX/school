from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.urls import reverse
from django_resized import ResizedImageField

from main.utils import main_image_random_name
from .managers import PostManager


User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_posts')
    overview = models.TextField()

    content = models.TextField(blank=True, null=True)
    main_image = ResizedImageField(size=[600, 350], blank=True, null=True,
                                   upload_to=main_image_random_name)
    active = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        permissions = [('author', 'Can add post')]
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def safe_content(self):
        return mark_safe(self.content)
