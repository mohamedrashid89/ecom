# Generated by Django 5.0.1 on 2024-01-10 06:18

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_remove_color_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None),
        ),
    ]
