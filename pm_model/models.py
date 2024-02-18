from django.db import models


# Create your models here.
class ArtificialProcess(models.Model):
    case_column = models.CharField(max_length=256, verbose_name='流程唯一标识列')
    activity_column = models.CharField(max_length=256, verbose_name='流程中动作列')
    timestamp_column = models.CharField(max_length=256, verbose_name='执行时间列')
    process_file = models.FileField(upload_to='pm_model/tmp_file', default="", verbose_name='执行时间列')

    class Meta:
        verbose_name = '人工处理'
        verbose_name_plural = '人工处理'
