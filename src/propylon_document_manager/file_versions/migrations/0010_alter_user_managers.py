# Generated by Django 5.0.1 on 2024-04-11 15:25

import propylon_document_manager.file_versions.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("file_versions", "0009_alter_user_managers"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", propylon_document_manager.file_versions.models.UserManager()),
            ],
        ),
    ]
