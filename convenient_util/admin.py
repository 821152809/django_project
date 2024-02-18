from django.contrib import admin
from convenient_util import models
from import_export.admin import ImportExportModelAdmin
import openpyxl


# Register your models here.
@admin.register(models.SQLUtil)
class DataProcess(ImportExportModelAdmin):
    # 列表页显示那些字段（列）
    list_display = [
        "table_name_en",
        "table_name_cn",
        "column_source",
        "table_lifecycle"
    ]
    search_fields = ["table_name_en", "table_name_cn", "column_source"]

    def generate_create_table_sql(modeladmin, request, queryset):
        for obj in queryset:
            list_records = []
            if obj.column_source == 0:
                column_list = obj.column_names.split("/")
                for info in column_list:
                    info_split = info.split(",")
                    field_name = info_split[0]
                    field_type = info_split[1]
                    field_comment = info_split[2]
                    list_records.append([field_name, field_type, field_comment])
            elif obj.column_source == 1:
                book = openpyxl.load_workbook(obj.column_file, data_only=True)
                sheet = book.worksheets[0]  # 取sheet 页，默认是0，可以根据自己需求进行调整
                list_records = []
                for row in sheet.rows:
                    row_val = [col.value for col in row]
                    field_name = row_val[0]
                    field_type = row_val[1]
                    field_comment = row_val[2]
                    list_records.append([field_name, field_type, field_comment])

            field_name_len_list = []
            field_type_len_list = []
            fill_value = " "
            for field in list_records:
                field_name_len = len(field[0])
                field_type_len = len(field[1])
                field_name_len_list.append(field_name_len)
                field_type_len_list.append(field_type_len)

            field_name_len_max = max(field_name_len_list) + 4
            field_typ_len_max = max(field_type_len_list) + 1
            create_table_ste = ""
            first_field_name = list_records[0][0]

            for s_field in list_records:
                field_name_len = len(s_field[0])
                field_type_len = len(s_field[1])
                if first_field_name == s_field[0]:
                    create_table_ste_tmp = (
                        "     "
                        + s_field[0].lower()
                        + fill_value * (field_name_len_max - field_name_len)
                        + s_field[1]
                        + fill_value * (field_typ_len_max - field_type_len)
                        + "comment '"
                        + s_field[2]
                        + "'\n"
                    )
                    create_table_ste += create_table_ste_tmp
                else:
                    create_table_ste_tmp = (
                        "    ,"
                        + s_field[0].lower()
                        + fill_value * (field_name_len_max - field_name_len)
                        + s_field[1]
                        + fill_value * (field_typ_len_max - field_type_len)
                        + "comment '"
                        + s_field[2]
                        + "'\n"
                    )
                    create_table_ste += create_table_ste_tmp

            before_str = (
                "create table if not exists "
                + obj.project_space_name
                + "."
                + obj.table_name_en
                + "("
                + "\n"
            )
            end_str = (
                ") comment '"
                + obj.table_name_cn
                + "' partitioned by (ds string) lifecycle "
                + str(obj.table_lifecycle)
                + ";"
            )

            obj.result = before_str + create_table_ste + end_str
            obj.save()

    def generate_create_table_and_di_merge_sql(modeladmin, request, queryset):
        for obj in queryset:
            list_records = []
            if obj.column_source == 0:
                column_list = obj.column_names.split("/")
                for info in column_list:
                    info_split = info.split(",")
                    field_name = info_split[0]
                    field_type = info_split[1]
                    field_comment = info_split[2]
                    list_records.append([field_name, field_type, field_comment])
            elif obj.column_source == 1:
                book = openpyxl.load_workbook(obj.column_file, data_only=True)
                sheet = book.worksheets[0]  # 取sheet 页，默认是0，可以根据自己需求进行调整
                list_records = []
                for row in sheet.rows:
                    row_val = [col.value for col in row]
                    field_name = row_val[0]
                    field_type = row_val[1]
                    field_comment = row_val[2]
                    list_records.append([field_name, field_type, field_comment])

            field_name_len_list = []
            field_type_len_list = []
            fill_value = " "
            for field in list_records:
                field_name_len = len(field[0])
                field_type_len = len(field[1])
                field_name_len_list.append(field_name_len)
                field_type_len_list.append(field_type_len)

            field_name_len_max = max(field_name_len_list) + 4
            field_name_len_max1 = max(field_name_len_list) + 1
            field_typ_len_max = max(field_type_len_list) + 1
            create_table_ste = ""
            first_field_name = list_records[0][0]

            for s_field in list_records:
                field_name_len = len(s_field[0])
                field_type_len = len(s_field[1])
                if first_field_name == s_field[0]:
                    create_table_ste_tmp = (
                        "     "
                        + s_field[0].lower()
                        + fill_value * (field_name_len_max - field_name_len)
                        + s_field[1]
                        + fill_value * (field_typ_len_max - field_type_len)
                        + "comment '"
                        + s_field[2]
                        + "'\n"
                    )
                    create_table_ste += create_table_ste_tmp
                else:
                    create_table_ste_tmp = (
                        "    ,"
                        + s_field[0].lower()
                        + fill_value * (field_name_len_max - field_name_len)
                        + s_field[1]
                        + fill_value * (field_typ_len_max - field_type_len)
                        + "comment '"
                        + s_field[2]
                        + "'\n"
                    )
                    create_table_ste += create_table_ste_tmp

            before_str = (
                "create table if not exists "
                + obj.project_space_name
                + "."
                + obj.table_name_en
                + "("
                + "\n"
            )
            end_str = (
                ") comment '"
                + obj.table_name_cn
                + "' partitioned by (ds string) lifecycle "
                + str(obj.table_lifecycle)
                + ";"
            )

            create_table_sql = before_str + create_table_ste + end_str

            """
                用于merge case when 代码合并的字符串拼接
            """
            merge_str = ""
            for s_field in list_records:
                field_name_len = len(s_field[0])
                if first_field_name == s_field[0]:
                    merge_str_tmp = (
                        "     "
                        + "case when di."
                        + first_field_name
                        + " is not null then di."
                        + s_field[0]
                        + " " * (field_name_len_max1 - field_name_len)
                        + "else "
                        + "df."
                        + s_field[0]
                        + " " * (field_name_len_max1 - field_name_len)
                        + "end "
                        + s_field[0]
                        + "\n"
                    )
                    merge_str += merge_str_tmp
                else:
                    merge_str_tmp = (
                        "    ,"
                        + "case when di."
                        + first_field_name
                        + " is not null then di."
                        + s_field[0]
                        + " " * (field_name_len_max1 - field_name_len)
                        + "else "
                        + "df."
                        + s_field[0]
                        + " " * (field_name_len_max1 - field_name_len)
                        + "end "
                        + s_field[0]
                        + "\n"
                    )
                    merge_str += merge_str_tmp

            df_str = ""
            for s_field in list_records:
                if first_field_name == s_field[0]:
                    df_str_tmp = "         " + s_field[0] + "\n"
                    df_str += df_str_tmp
                else:
                    df_str_tmp = "        ," + s_field[0] + "\n"
                    df_str += df_str_tmp

            di_finally_str = (
                "    select"
                + "\n"
                + df_str
                + "    from "
                + obj.project_space_name
                + "."
                + obj.table_name_en
                + "_delta"
                + "\n"
                "    where ds = ${today}"
            )

            df_finally_str = (
                "    select"
                + "\n"
                + df_str
                + "    from "
                + obj.project_space_name
                + "."
                + obj.table_name_en
                + "\n"
                "    where ds = ${yesterday}"
            )

            finally_statement = (
                "insert overwrite table "
                + obj.table_name_en
                + " partition (ds=${today})"
                + "\n"
                + "select"
                + "\n"
                + merge_str
                + "from ("
                + "\n"
                + di_finally_str
                + "\n"
                + ") di"
                + "\n"
                + "full join ("
                + "\n"
                + df_finally_str
                + "\n"
                + ") df on di."
                + first_field_name
                + " = df."
                + first_field_name
                + ";"
            )
            obj.result = create_table_sql + "\n" + finally_statement
            obj.save()

    generate_create_table_sql.short_description = "生成建表语句"
    generate_create_table_and_di_merge_sql.short_description = "生成建表语句和增量合并语句"
    actions = [generate_create_table_sql, generate_create_table_and_di_merge_sql]
