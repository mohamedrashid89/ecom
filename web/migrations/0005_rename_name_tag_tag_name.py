# Generated by Django 5.0.1 on 2024-01-07 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_rename_name_color_status_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='name',
            new_name='tag_name',
        ),
    ]
