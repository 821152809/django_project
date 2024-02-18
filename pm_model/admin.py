from django.contrib import admin

from pm_model import models


# Register your models here.
# admin.site.register(models.ArtificialProcess)

@admin.register(models.ArtificialProcess)
class DataProcess(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ['id', 'case_column', 'activity_column', 'timestamp_column', 'process_file']

    def start_analysis(self, request, queryset):
        # queryset.update(status='d')
        for info in queryset:
            print(info)

    start_analysis.short_description = "开始分析"
    actions = [start_analysis]

