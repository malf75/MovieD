# Generated by Django 5.0.1 on 2024-01-27 02:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0009_remove_postagem_usuario_postagem_numero_usuario_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postagem',
            name='numero_usuario',
        ),
        migrations.AddField(
            model_name='postagem',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comentarios', to=settings.AUTH_USER_MODEL),
        ),
    ]
