# Generated by Django 4.1 on 2024-01-26 06:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("convenient_util", "0009_alter_sqlutil_column_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sqlutil",
            name="column_names",
            field=models.TextField(
                blank=True,
                default="",
                max_length=512,
                verbose_name="字段内容(格式：name,type,comment/name,type,comment)",
            ),
        ),
    ]