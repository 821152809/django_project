import json

import pandas as pd
import base64
import hmac
import time
import uuid
from urllib import parse
import requests


ak = "fa29a418-542d-4823-bd83-205a765c93fb"
sk = "bed83a6c-d892-4f83-93b9-c91d898050f7"
# QBI域名
host = "http://quickbi.feihe.com"


# 读文件
def read_file(file_path):
    str_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        line = file.readline()
        while line:
            # 处理每一行的逻辑
            str_list.append(line.replace("\r\n", "").replace("\n", ""))
            line = file.readline()
    return str_list


# sha256加密
def hash_hmac(key, code, algorithm="sha256"):
    hmac_code = hmac.new(key.encode("UTF-8"), code.encode("UTF-8"), algorithm).digest()
    return base64.b64encode(hmac_code).decode()


# 生成签名
def signature(method, uri, params, ak, sk, uuid_str, timestamp):
    # Request参数拼接
    if not bool(params):
        request_query = ""
    else:
        request_query = "\n"
        for i in sorted(params):
            if bool(params[i]):
                request_query = request_query + i + "=" + str(params[i]) + "&"
    request_query = request_query.strip("&")
    # Request的Header拼接
    headers = (
        "\nX-Gw-AccessId:"
        + ak
        + "\nX-Gw-Nonce:"
        + str(uuid_str)
        + "\nX-Gw-Timestamp:"
        + str(timestamp)
    )
    # 待签名字符串
    StringToSign = method.upper() + "\n" + uri + request_query + headers
    encode_string = parse.quote(StringToSign, "")
    sign = hash_hmac(sk, encode_string)
    return sign


# 调用QBI接口查询数据集信息
def query_dataset_info(dataset_id):
    # 接口路径
    uri = "/openapi/v2/dataset/infoNew"
    url = host + uri

    # json传参
    jsonParam = {"datasetId": dataset_id}
    # 表单传参
    formParams = {
        "datasetId": dataset_id,
    }
    # 生成签名
    # 生成随机数
    uuid_str = str(uuid.uuid1())
    # 请求时间戳 UNIX时间戳，13位
    time_unix = str(round(time.time() * 1000))
    sign = signature("GET", uri, formParams, ak, sk, uuid_str, time_unix)

    headers = {
        "X-Gw-AccessId": ak,
        "X-Gw-Nonce": uuid_str,
        "X-Gw-Timestamp": time_unix,
        "X-Gw-Signature": sign,
        # 开启调试
        "X-Gw-Debug": "true",
        "Content-Type": "application/json",
    }
    response = requests.request(
        method="GET", url=url, headers=headers, params=formParams, json=jsonParam
    )
    return json.loads(response.content.decode("utf-8")).get("data")


# 调用qbi接口获取返回结果
def query_works_blood_relationship(works_id):
    # 接口路径
    uri = "/openapi/v2/works/bloodRelationship"
    url = host + uri

    # json传参
    jsonParam = {"worksId": works_id}
    # 表单传参
    formParams = {
        "worksId": works_id,
    }
    # 生成签名
    # 生成随机数
    uuid_str = str(uuid.uuid1())
    # 请求时间戳 UNIX时间戳，13位
    time_unix = str(round(time.time() * 1000))
    sign = signature("GET", uri, formParams, ak, sk, uuid_str, time_unix)

    headers = {
        "X-Gw-AccessId": ak,
        "X-Gw-Nonce": uuid_str,
        "X-Gw-Timestamp": time_unix,
        "X-Gw-Signature": sign,
        # 开启调试
        "X-Gw-Debug": "true",
        "Content-Type": "application/json",
    }

    response = requests.request(
        method="GET", url=url, headers=headers, params=formParams, json=jsonParam
    )
    return json.loads(response.content.decode("utf-8"))


# 数据集解析
def data_set_analysis(dataset_info):
    # 维度字段信息
    dimension_list = dataset_info.get("dimensionList")
    column_list = []
    for dimension in dimension_list:
        dimension_type = dimension.get("dimensionType")
        if dimension_type is not None:
            if dimension_type == "standard_dimension":
                dimension_type = "维度标准字段"
            elif dimension_type == "calculate_dimension":
                dimension_type = "维度计算字段"

        data_type = dimension.get("dataType")
        if data_type is not None:
            if data_type == "string":
                data_type = "字符串类型"
            elif data_type == "datetime":
                data_type = "日期类型"

        new_column_dict = {
            "项目空间名称": dataset_info.get("workspaceName"),
            # "数据源名称": info_json_obj.get("dsName"),
            # "数据源ID": info_json_obj.get("dsId"),
            # "数据源类型": info_json_obj.get("dsType"),
            # "责任人名称": info_json_obj.get("ownerName"),
            "数据集名称": dataset_info.get("datasetName"),
            # "数据集ID": info_json_obj.get("datasetId"),
            "字段ID": dimension.get("uid"),
            "字段中文名称": dimension.get("caption"),
            "字段英文名称": dimension.get("factColumn"),
            "字段类型": dimension_type,
            "字段数据类型": data_type,
            # "字段粒度": dimension.get("granularity"),
            "计算公式": dimension.get("expression"),
        }
        column_list.append(new_column_dict)

    # 计算字段信息
    measure_list = dataset_info.get("measureList")
    for measure in measure_list:
        measure_type = measure.get("measureType")
        if measure_type is not None:
            if measure_type == "standard_measure":
                measure_type = "度量标准字段"
            elif measure_type == "calculate_measure":
                measure_type = "度量计算字段"

        data_type = measure.get("dataType")
        if data_type is not None:
            if data_type == "number":
                data_type = "数值类型"
            elif data_type == "string":
                data_type = "字符串类型"
        new_column_dict = {
            "项目空间名称": dataset_info.get("workspaceName"),
            # "数据源名称": info_json_obj.get("dsName"),
            # "数据源ID": info_json_obj.get("dsId"),
            # "数据源类型": info_json_obj.get("dsType"),
            # "责任人名称": info_json_obj.get("ownerName"),
            "数据集名称": dataset_info.get("datasetName"),
            # "数据集ID": info_json_obj.get("datasetId"),
            "字段ID": measure.get("uid"),
            "字段中文名称": measure.get("caption"),
            "字段英文名称": measure.get("factColumn"),
            "字段类型": measure_type,
            "字段数据类型": data_type,
            # "字段粒度": measure.get("granularity"),
            "计算公式": measure.get("expression"),
        }
        column_list.append(new_column_dict)
    return column_list


def base_and_qbi_merge(base_exp_data_path):
    # 读数据库导出的数据
    base_info = pd.read_excel(base_exp_data_path)
    base_info_list = []
    for info in base_info.values:
        space_name = info[0]
        cube_show_name = info[1]
        source_table = info[2]
        page_id = info[3]
        page_name = info[4]
        page_type = info[5]
        # 调用QBI接口获取报表信息
        print(page_id)
        if page_id is not None or page_id != "nan":
            query_info = query_works_blood_relationship(page_id)
            message = query_info.get("message")
            data = query_info.get("data")
            base_info_dict = {
                "项目空间名称": space_name,
                "数据集名称": cube_show_name,
                "页面ID": page_id,
                "页面名称": page_name,
                "页面类型": page_type,
                "接口返回信息": message,
                "接口返回数据": data,
            }
            base_info_list.append(base_info_dict)
    return base_info_list


# json解析
def qbi_return_json_analysis(page_info_list):
    param_list = []
    for page_info in page_info_list:
        queryParams = page_info.get("queryParams")
        if len(queryParams) > 0:
            for queryParam in queryParams:
                param_dict = {
                    "字段ID": queryParam.get("pathId"),
                    "字段中文名称": queryParam.get("caption"),
                    "字段类型": queryParam.get("areaName"),
                }
                param_list.append(param_dict)
    return param_list


"""
业务场景：若隐藏或清除QBI某数据集字段，评估下游影响，当前仅可评估已发布或曾经发布的数据集，获取的信息为发布后的内容
1.使用数据集ID调用QBI接口获取数据集基础信息，数据集ID需要从QBI的地址栏获取
2.从数据库获取数据集下游报表，生成base_exp_data_path参数
select distinct space_name, cube_show_name, source_table, page_id, page_name
        ,CASE
            WHEN page_type = 'dashboardOfflineQuery' then '自助取数'
            WHEN page_type = 'REPORT' then '电子表格'
            WHEN page_type = 'PAGE' then '仪表板' 
            ELSE null
        end page_type_name
    from qbi.ads_cube_basic_information_df
    where source_table like "%表名%" and space_name ='空间名' and cube_show_name = '数据集名' and page_id is not null
3.通过步骤2的page_id调用QBI接口获取返回结果
4.获取想要匹配的数据集的字段
"""

if __name__ == "__main__":
    # 需要处理的字段
    process_column_list = [
        "是否猎洋门店",
        "是否为大系统",
        "TOP3系统",
        "飞鹤第几主推",
        "飞鹤主推品项",
        "超级门店",
        "是否裸价",
        "1_N_X",
        "门店奶容",
        "是否为top3系统",
        "是否星飞帆卓护数字化门店",
        "星飞帆卓护数字化首次上架日期",
        "淳芮A2数字化商品状态",
        "淳芮A2数字化首次上架日期",
        "星飞帆卓护是否可比",
        "淳芮A2是否可比",
        "是否淳芮A2数字化动销门店",
        "是否星飞帆卓护数字化动销门店",
        "新客人数",
        "新客销售额",
        "米粉新客人数",
    ]

    # 调用QBI接口查询数据集信息
    dataset_id = "c6b620a9-7b02-447c-9364-df9b26959801"
    print("数据集ID:" + dataset_id)
    dataset_info = query_dataset_info(dataset_id)
    # 数据集字段信息
    data_set_column_list = data_set_analysis(dataset_info)
    print("查询完成,已获取数据集信息")
    print("-------------------------------------------")
    print("进行拟删字段匹配查询")
    match_data_set_column_list = []
    match_column_list = []
    for info in data_set_column_list:
        if info.get("字段中文名称") in process_column_list:
            match_column_list.append(info.get("字段中文名称"))
            match_data_set_column_list.append(info)
    difference = list(set(process_column_list) - set(match_column_list))
    if len(difference) > 0:
        print("未在数据集中查到字段:" + ",".join(difference))
    else:
        print("已找到所有提供的字段")
    print("-------------------------------------------")
    print("根据数据库查询结果进行QBI接口调用,获取报表信息")
    # 数据库导出的内容与QBI返回的结果进行合并
    base_exp_data_path = "C:\\Users\\Administrator\\Desktop\\市场部经营业绩基础表字段血缘\\结果集.xlsx"
    base_info_list = base_and_qbi_merge(base_exp_data_path)
    print("区分qbi接口返回异常与正常数据")
    release_list = []
    not_release_list = []
    for base_info in base_info_list:
        message = base_info.get("接口返回信息")
        data = base_info.get("接口返回数据")
        if "success" == message:
            release_list.append(base_info)
        else:
            not_release_list.append(base_info)
    print("区分完成")
    print("-------------------------------------------")

    result_list = [["项目空间名称", "数据集名称", "页面名称", "页面类型", "处理结果"]]
    for page_info in not_release_list:
        result_list.append(
            [
                page_info.get("项目空间名称"),
                page_info.get("数据集名称"),
                page_info.get("页面名称"),
                page_info.get("页面类型"),
                page_info.get("接口返回信息"),
            ]
        )
    print("-------------------------------------------")
    print("开始进行正常数据处理")
    for page_info in release_list:
        # 解析返回内容
        analysis_column_list = qbi_return_json_analysis(page_info.get("接口返回数据"))
        column_result_info_list = []
        for column_info in analysis_column_list:
            page_column_id = column_info.get("字段ID")
            for match_data_set_column in match_data_set_column_list:
                if page_column_id == match_data_set_column.get("字段ID"):
                    # print(page_info)
                    # print(match_data_set_column)
                    # print(column_info)
                    process_dict = {
                        "字段中文名称": match_data_set_column.get("字段中文名称"),
                        "字段英文名称": match_data_set_column.get("字段英文名称"),
                        "字段类型": match_data_set_column.get("字段类型"),
                        "字段数据类型": match_data_set_column.get("字段数据类型"),
                        # "字段粒度":match_data_set_column.get('字段粒度'),
                        "计算公式": match_data_set_column.get("计算公式"),
                        "应用场景": column_info.get("字段类型"),
                    }
                    column_result_info_list.append(process_dict)
        if len(column_result_info_list) == 0:
            process_result = "无待处理字段"
        else:
            process_result = column_result_info_list
        result_list.append(
            [
                page_info.get("项目空间名称"),
                page_info.get("数据集名称"),
                page_info.get("页面名称"),
                page_info.get("页面类型"),
                process_result,
            ]
        )

    # 将结果集写入文件
    df = pd.DataFrame(result_list)
    df.to_excel(
        "C:\\Users\\Administrator\\Desktop\\市场部经营业绩基础表字段血缘\\result.xlsx",
        index=False,
        header=False,
    )
    print('处理完成，已将结果写入文件')
