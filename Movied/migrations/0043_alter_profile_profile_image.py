# Generated by Django 5.0.1 on 2024-03-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0042_alter_filmes_series_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
