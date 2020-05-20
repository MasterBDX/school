# Generated by Django 3.0.3 on 2020-05-19 23:45

from django.db import migrations
import django_resized.forms
import posts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='main_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=0, size=[600, 350], upload_to=posts.utils.main_image_random_name),
        ),
    ]
