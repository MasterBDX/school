# Generated by Django 3.0.3 on 2020-05-14 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_tabels', '0005_auto_20200514_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='en_subject',
        ),
    ]
