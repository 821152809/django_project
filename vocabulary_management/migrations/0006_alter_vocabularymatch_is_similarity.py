# Generated by Django 4.1 on 2023-09-04 00:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vocabulary_management", "0005_alter_vocabularymatch_match_threshold"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vocabularymatch",
            name="is_similarity",
            field=models.IntegerField(
                choices=[(0, "是"), (1, "否")], default=0, verbose_name="是否启用相似度匹配"
            ),
        ),
    ]
