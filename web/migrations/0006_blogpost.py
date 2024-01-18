# Generated by Django 5.0.1 on 2024-01-08 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_rename_name_tag_tag_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Post/')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quote', models.CharField(max_length=200)),
                ('Person_name', models.CharField(max_length=20)),
                ('tags', models.ManyToManyField(to='web.tag')),
            ],
        ),
    ]
