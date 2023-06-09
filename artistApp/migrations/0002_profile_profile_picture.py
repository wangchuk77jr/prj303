# Generated by Django 4.2 on 2023-05-15 10:35

import artistApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default=artistApp.models.default_avatar, null=True, upload_to='profile_pics'),
        ),
    ]
