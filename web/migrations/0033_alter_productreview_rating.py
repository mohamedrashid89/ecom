# Generated by Django 5.0.1 on 2024-01-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_alter_productreview_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=None),
        ),
    ]
