# Generated by Django 4.1 on 2023-09-04 00:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VocabularyManagement",
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
                (
                    "vocabulary_en",
                    models.CharField(max_length=256, verbose_name="词汇英文"),
                ),
                (
                    "vocabulary_cn",
                    models.CharField(max_length=256, verbose_name="词汇中文"),
                ),
                (
                    "timestamp_column",
                    models.CharField(max_length=256, verbose_name="执行时间列"),
                ),
                (
                    "process_file",
                    models.FileField(
                        default="", upload_to="pm_model/tmp_file", verbose_name="执行时间列"
                    ),
                ),
            ],
            options={
                "verbose_name": "词汇管理",
                "verbose_name_plural": "词汇管理",
            },
        ),
    ]
