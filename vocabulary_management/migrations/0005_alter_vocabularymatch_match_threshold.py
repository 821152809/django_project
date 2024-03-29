# Generated by Django 4.1 on 2023-09-04 00:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vocabulary_management", "0004_vocabularymatch"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vocabularymatch",
            name="match_threshold",
            field=models.FloatField(
                default=0.85,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(1.0),
                ],
                verbose_name="阈值",
            ),
        ),
    ]
