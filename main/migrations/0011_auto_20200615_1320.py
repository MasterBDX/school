# Generated by Django 3.0.3 on 2020-06-15 13:20

from django.db import migrations
import django_resized.forms
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200510_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainarticle',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=0, size=[600, 600], upload_to=main.utils.article_image_random_name),
        ),
    ]
