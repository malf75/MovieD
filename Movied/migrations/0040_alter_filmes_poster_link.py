# Generated by Django 5.0.1 on 2024-02-24 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0039_alter_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmes',
            name='Poster_Link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
