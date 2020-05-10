from django.db import models
from django.utils.safestring import mark_safe
from django_resized import ResizedImageField


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

    def safe_content(self):
        return mark_safe(self.content)


class MainArticle(models.Model):
    image = ResizedImageField(size=[600, 600], blank=True, null=True)
    title = models.CharField(max_length=255)
    english_title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    english_desc = models.TextField(null=True, blank=True)
