# Generated by Django 5.0.1 on 2024-03-10 20:35

import Movied.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0044_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=Movied.models.user_directory_path),
        ),
    ]