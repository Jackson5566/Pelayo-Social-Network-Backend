# Generated by Django 4.2.4 on 2023-09-12 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("message_app", "0003_remove_messagesmodel_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="messagesmodel",
            name="content",
            field=models.CharField(
                error_messages={
                    "max_length": "El límite de texto impuesto es de 10000 caracteres, no puede exceder"
                },
                max_length=10000,
            ),
        ),
    ]
