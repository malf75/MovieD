# Generated by Django 5.0.1 on 2024-02-06 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0019_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=80, null=True),
        ),
    ]