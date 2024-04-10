# Generated by Django 5.0.1 on 2024-04-10 22:22

import propylon_document_manager.file_versions.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file_versions", "0002_fileversion_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileversion",
            name="file",
            field=models.FileField(
                blank=True, null=True, upload_to=propylon_document_manager.file_versions.models.get_upload_to
            ),
        ),
    ]