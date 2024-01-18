# Generated by Django 5.0.1 on 2024-01-08 06:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_blogpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='tags',
        ),
        migrations.AddField(
            model_name='tag',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.blogpost'),
        ),
    ]
