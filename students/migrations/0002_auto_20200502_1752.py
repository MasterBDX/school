# Generated by Django 3.0.3 on 2020-05-02 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_tabels', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultspaper',
            name='the_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='school_tabels.TheClass'),
            preserve_default=False,
        ),
    ]
