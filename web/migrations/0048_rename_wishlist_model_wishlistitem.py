# Generated by Django 5.0.1 on 2024-01-29 06:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0047_tag_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wishlist_model',
            new_name='WishlistItem',
        ),
    ]
