# Generated by Django 5.0.1 on 2024-01-10 06:00

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0022_rename_status_color_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None),
        ),
    ]
