from django.db import models
from django.core.files.storage import FileSystemStorage


class SQLUtil(models.Model):
    table_name_en = models.CharField(
        max_length=256, blank=True, default="table_name", verbose_name="表英文名称"
    )
    table_name_cn = models.CharField(
        max_length=256, blank=True, default="表注释", verbose_name="表中文名称"
    )
    project_space_name = models.CharField(
        max_length=256, blank=True, default="firmus_dataphin_prd_ods", verbose_name="项目空间"
    )
    column_source = models.IntegerField(
        choices=((0, "内容"), (1, "文件")), default=1, verbose_name="字段来源"
    )
    table_lifecycle = models.IntegerField(default=90, verbose_name="表生命周期")
    column_names = models.TextField(
        max_length=10240,
        blank=True,
        null=False,
        default="",
        verbose_name="字段内容(格式：name,type,comment/name,type,comment)",
    )
    column_file = models.FileField(
        blank=True,
        default="",
        storage=FileSystemStorage(location="{DIR_PATH}/".format(DIR_PATH="DIR_PATH")),
        upload_to="convenient_util/column_file_dir",
        verbose_name="字段文件",
    )
    result = models.TextField(
        max_length=10240,
        blank=True,
        null=False,
        default="",
        verbose_name="拼接结果",
    )

    class Meta:
        verbose_name = "建表语句生成工具"
        verbose_name_plural = "建表语句生成工具"
