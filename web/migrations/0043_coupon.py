# Generated by Django 5.0.1 on 2024-01-23 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0042_address_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
