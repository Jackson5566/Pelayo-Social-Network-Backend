# Generated by Django 4.2.4 on 2024-01-23 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_remove_user_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=50),
        ),
    ]
