# Generated by Django 3.0.3 on 2020-05-06 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200506_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolinfo',
            name='city',
            field=models.CharField(default='houn', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolinfo',
            name='province',
            field=models.CharField(default='aljufra', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolinfo',
            name='street',
            field=models.CharField(default='baba', max_length=255),
            preserve_default=False,
        ),
    ]
