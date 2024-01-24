# Generated by Django 5.0.1 on 2024-01-22 14:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0004_userroleroutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ban_end_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ban_start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_user_banned',
            field=models.BooleanField(default=False),
        ),
    ]
