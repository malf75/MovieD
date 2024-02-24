# Generated by Django 5.0.1 on 2024-02-09 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0032_postagem_filmes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postagem',
            name='filmes',
        ),
        migrations.AddField(
            model_name='filmes',
            name='postagens',
            field=models.ManyToManyField(blank=True, related_name='filmes', to='Movied.postagem'),
        ),
    ]