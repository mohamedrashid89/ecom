# Generated by Django 5.0.1 on 2024-01-15 05:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0036_address_alter_cartorder_product_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wishlist',
            new_name='Wishlist_model',
        ),
    ]