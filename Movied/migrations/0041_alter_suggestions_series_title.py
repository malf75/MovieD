# Generated by Django 5.0.1 on 2024-02-24 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0040_alter_filmes_poster_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestions',
            name='Series_Title',
            field=models.CharField(max_length=120),
        ),
    ]