# Generated by Django 5.0.1 on 2024-01-10 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_alter_color_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='status',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
