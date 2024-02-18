from django.contrib import admin

from vocabulary_management import models
from vocabulary_management.logic.language_trans import LanguageTrans
from import_export.admin import ImportExportModelAdmin
import difflib


admin.site.site_header = "飞鹤-数据中心组后台管理系统"
admin.site.index_title = "首页"


@admin.register(models.VocabularyManagement)
class DataProcess(ImportExportModelAdmin):
    # 列表页显示那些字段（列）
    list_display = [
        "vocabulary_en",
        "vocabulary_cn",
        "vocabulary_type",
        "vocabulary_desc",
    ]
    search_fields = [
        "vocabulary_en",
        "vocabulary_cn",
    ]


@admin.register(models.VocabularyTranslate)
class DataProcess(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ["vocabulary", "trans_mode", "trans_result", "trans_result_lower"]
    list_filter = ("vocabulary",)
    search_fields = ["vocabulary"]

    def start_trans(modeladmin, request, queryset):
        for obj in queryset:
            if obj.trans_mode == 0:
                trans_mode_in = "E2C"
            else:
                trans_mode_in = "C2E"
            translator = LanguageTrans(trans_mode_in)
            trans_result = translator.trans(obj.vocabulary)
            obj.trans_result = trans_result
            obj.trans_result_lower = trans_result.lower()
            obj.save()

    def add_vocabulary_base(modeladmin, request, queryset):
        for obj in queryset:
            """"""

    start_trans.short_description = "开始翻译"
    # add_vocabulary_base.short_description = "添加至词汇库"
    actions = [start_trans]


@admin.register(models.VocabularyMatch)
class DataProcess(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ["vocabulary", "match_result"]
    search_fields = ["vocabulary"]

    def start_match(modeladmin, request, queryset):
        for obj in queryset:
            vocabulary = obj.vocabulary
            vocabulary_type = obj.vocabulary_type
            is_similarity = obj.is_similarity
            match_result_num = obj.match_result_num

            vm_model_all = models.VocabularyManagement.objects.all()
            vm_all = []
            # vocabulary_type根据类型判断是匹配英文还是中文
            for vm_model in vm_model_all:
                if vocabulary_type == 0:
                    vm_all.append(vm_model.vocabulary_en)
                else:
                    vm_all.append(vm_model.vocabulary_cn)

            # 若使用相似度匹配
            if is_similarity == 0:
                match_threshold = obj.match_threshold
                # 相似度匹配
                match_vm_top = difflib.get_close_matches(
                    vocabulary, vm_all, n=match_result_num, cutoff=match_threshold
                )
                obj.match_result = ",".join(match_vm_top)
            else:
                match_mode = obj.match_mode
                match_vm_top = []
                current_num = 0
                for vm in vm_all:
                    if match_mode == 0:
                        if vocabulary in vm:
                            match_vm_top.append(vm)
                    elif match_mode == 1:
                        if vocabulary == vm:
                            match_vm_top.append(vm)
                    elif match_mode == 2:
                        if str(vm).startswith(vocabulary):
                            match_vm_top.append(vm)
                    elif match_mode == 3:
                        if str(vm).endswith(vocabulary):
                            match_vm_top.append(vm)
                    current_num += 1
                    if current_num == match_result_num:
                        break
                obj.match_result = ",".join(match_vm_top)
            obj.save()

    start_match.short_description = "开始匹配"
    actions = [start_match]
