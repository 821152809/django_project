# Generated by Django 4.1 on 2023-09-04 01:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("vocabulary_management", "0013_vocabularytranslate_vocabulary_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vocabularytranslate",
            old_name="vocabulary_type",
            new_name="trans_mode",
        ),
    ]
