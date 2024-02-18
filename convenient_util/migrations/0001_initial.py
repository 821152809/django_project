# Generated by Django 4.1 on 2024-01-16 00:58

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SQLUtil",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_name", models.CharField(max_length=256, verbose_name="任务名称")),
                (
                    "column_names",
                    models.CharField(max_length=256, verbose_name="需处理的字段"),
                ),
            ],
            options={
                "verbose_name": "SQL工具",
                "verbose_name_plural": "SQL工具",
            },
        ),
    ]
