# Generated by Django 5.0.1 on 2024-04-11 08:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file_versions", "0005_alter_fileversion_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fileversion",
            name="version_number",
            field=models.IntegerField(null=True),
        ),
    ]
