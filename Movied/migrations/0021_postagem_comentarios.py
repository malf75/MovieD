# Generated by Django 5.0.1 on 2024-02-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0020_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='postagem',
            name='comentarios',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
    ]
