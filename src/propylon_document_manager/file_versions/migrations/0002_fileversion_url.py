# Generated by Django 5.0.1 on 2024-04-08 21:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file_versions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileversion",
            name="url",
            field=models.CharField(default="storage", max_length=2048),
        ),
    ]
