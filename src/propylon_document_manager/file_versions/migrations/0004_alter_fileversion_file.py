# Generated by Django 5.0.1 on 2024-04-10 22:48

import propylon_document_manager.file_versions.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file_versions", "0003_fileversion_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fileversion",
            name="file",
            field=models.FileField(blank=True, upload_to=propylon_document_manager.file_versions.models.get_upload_to),
        ),
    ]
