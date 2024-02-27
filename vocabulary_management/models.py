from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.files.storage import FileSystemStorage


class VocabularyManagement(models.Model):
    vocabulary_en = models.CharField(max_length=256, verbose_name="词汇英文")
    vocabulary_cn = models.CharField(max_length=256, verbose_name="词汇中文")
    vocabulary_type = models.IntegerField(
        choices=((0, "业务"), (1, "技术"), (2, "管理")), default=0, verbose_name="词汇类别"
    )
    vocabulary_desc = models.TextField(
        max_length=512, blank=True, null=False, default="", verbose_name="词汇备注"
    )

    class Meta:
        verbose_name = "词汇管理"
        verbose_name_plural = "词汇管理"


class VocabularyTranslate(models.Model):
    vocabulary = models.CharField(max_length=256, verbose_name="词汇")
    trans_mode = models.IntegerField(
        choices=((0, "英译汉"), (1, "汉译英")), default=0, verbose_name="翻译模式"
    )
    trans_result = models.CharField(
        editable=False, max_length=256, blank=True, null=False, verbose_name="翻译结果"
    )
    trans_result_lower = models.CharField(
        editable=False, max_length=256, blank=True, null=False, verbose_name="翻译结果(小写)"
    )

    class Meta:
        verbose_name = "词汇翻译"
        verbose_name_plural = "词汇翻译"


class VocabularyMatch(models.Model):
    vocabulary = models.CharField(max_length=256, verbose_name="词汇")
    vocabulary_type = models.IntegerField(
        choices=((0, "英文"), (1, "中文")), default=0, verbose_name="词汇类别"
    )
    is_similarity = models.IntegerField(
        choices=((0, "是"), (1, "否")),
        default=0,
        verbose_name="是否启用相似度匹配",
    )
    match_threshold = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.85,
        verbose_name="阈值",
    )
    match_mode = models.IntegerField(
        choices=((0, "包含匹配"), (1, "精准匹配"), (2, "前缀匹配"), (3, "后缀匹配")),
        default=0,
        verbose_name="翻译模式",
    )
    match_result_num = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=False,
        default=5,
        verbose_name="匹配数量",
    )
    match_result = models.CharField(
        editable=False, max_length=256, blank=True, null=False, verbose_name="匹配结果"
    )

    class Meta:
        verbose_name = "词汇匹配"
        verbose_name_plural = "词汇匹配"


class VocabularyFileMatch(models.Model):
    vocabulary_file = models.FileField(
        blank=True,
        default="",
        storage=FileSystemStorage(location="{DIR_PATH}/".format(DIR_PATH="DIR_PATH")),
        upload_to="vocabulary_management/vocabulary_file_dir",
        verbose_name="词汇源文件",
    )
    result_file_path = models.CharField(
        max_length=256, blank=True, null=False, verbose_name="匹配结果数据路径"
    )

    class Meta:
        verbose_name = "词汇文件匹配"
        verbose_name_plural = "词汇文件匹配"
