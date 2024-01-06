# Generated by Django 4.2.4 on 2024-01-06 19:28

from django.db import migrations
import imagekit.models.fields
import posts_app.custom


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0013_user_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_photo',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, storage=posts_app.custom.FirebaseStorage(), upload_to='images/user'),
        ),
    ]
