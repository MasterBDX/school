from django.db import models
from django.utils.safestring import mark_safe
from django_resized import ResizedImageField
from django.utils.translation import get_language


from .utils import article_image_random_name

class SchoolInfo(models.Model):
    name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    school_phone = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_name(self):
        if get_language() == 'ar':
            name = self.name
        else:
            name = self.english_name
        return name


    def safe_content(self):
        return mark_safe(self.content)


class MainArticle(models.Model):
    image = ResizedImageField(size=[600, 600], blank=True, null=True,upload_to=article_image_random_name)
    title = models.CharField(max_length=255)
    english_title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    english_desc = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.title