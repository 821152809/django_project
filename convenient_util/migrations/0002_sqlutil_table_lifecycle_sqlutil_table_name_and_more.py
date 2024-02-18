# Generated by Django 4.1 on 2024-01-16 01:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("convenient_util", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sqlutil",
            name="table_lifecycle",
            field=models.IntegerField(default=0, verbose_name="表生命周期"),
        ),
        migrations.AddField(
            model_name="sqlutil",
            name="table_name",
            field=models.CharField(default="", max_length=256, verbose_name="表名称"),
        ),
        migrations.AlterField(
            model_name="sqlutil",
            name="column_names",
            field=models.TextField(
                default="",
                max_length=512,
                verbose_name="字段内容(格式：name,type,comment/name,type,comment)",
            ),
        ),
    ]