# Generated by Django 4.2.4 on 2023-11-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts_app", "0012_remove_postmodel_content_list_contentlistmodel_posts"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contentlistmodel",
            name="posts",
        ),
        migrations.AddField(
            model_name="postmodel",
            name="contents_list",
            field=models.ManyToManyField(
                blank=True,
                default=None,
                null=True,
                related_name="posts",
                to="posts_app.contentlistmodel",
            ),
        ),
    ]
