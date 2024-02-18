# Generated by Django 4.1.3 on 2022-11-24 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pm_model", "0004_alter_artificialprocess_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="artificialprocess",
            name="process_file",
            field=models.FileField(
                default="", upload_to="pm_model/tmp_file", verbose_name="执行时间列"
            ),
        ),
        migrations.AlterField(
            model_name="artificialprocess",
            name="activity_column",
            field=models.CharField(max_length=256, verbose_name="流程中动作列"),
        ),
        migrations.AlterField(
            model_name="artificialprocess",
            name="case_column",
            field=models.CharField(max_length=256, verbose_name="流程唯一标识列"),
        ),
    ]