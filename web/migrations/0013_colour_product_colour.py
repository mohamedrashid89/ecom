# Generated by Django 5.0.1 on 2024-01-09 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_rename_code_color_status_color_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='colour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.colour'),
        ),
    ]
