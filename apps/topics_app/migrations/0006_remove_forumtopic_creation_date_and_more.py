# Generated by Django 5.0.1 on 2024-01-24 20:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics_app', '0005_alter_forumtopic_creation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumtopic',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='forumtopic',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
