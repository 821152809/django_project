# Generated by Django 4.1 on 2023-09-04 01:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vocabulary_management", "0012_alter_vocabularytranslate_trans_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="vocabularytranslate",
            name="vocabulary_type",
            field=models.IntegerField(
                choices=[(0, "英译汉"), (1, "汉译英")], default=0, verbose_name="翻译模式"
            ),
        ),
    ]
