# Generated by Django 5.0.1 on 2024-01-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_remove_tag_post_blogpost_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]
