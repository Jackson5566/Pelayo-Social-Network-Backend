# Generated by Django 4.2.4 on 2023-08-06 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postmodel',
            old_name='disslikes',
            new_name='dislikes',
        ),
    ]
