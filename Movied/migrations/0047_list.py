# Generated by Django 5.0.1 on 2024-03-11 05:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movied', '0046_alter_notification_notification_sender_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filmes', models.ManyToManyField(blank=True, related_name='lists', to='Movied.filmes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='List_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]