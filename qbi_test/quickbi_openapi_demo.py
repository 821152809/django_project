import base64
import hmac
import time
import uuid
from urllib import parse
import requests

# 获取账户 AccessID 以及 AccessKey 注意防止泄露
# 实际来源 QUICK BI平台的识别码：AccessKey ID，AccessKey Secret
AccessID = "fa29a418-542d-4823-bd83-205a765c93fb"
AccessKey = "bed83a6c-d892-4f83-93b9-c91d898050f7"


# Base64编码下HMAC-SHA1计算值
def hash_hmac(key, code, algorithm="sha256"):
    hmac_code = hmac.new(key.encode("UTF-8"), code.encode("UTF-8"), algorithm).digest()
    return base64.b64encode(hmac_code).decode()


# 构造签名
def Signature(Method, URI, Params, AKID, AKSecret, UUID, timestamp):
    # Request参数拼接
    if not bool(Params):
        Request_QueryString = ""
    else:
        list = sorted(Params)
        Request_QueryString = "\n"
        for i in list:
            if bool(Params[i]):
                Request_QueryString = (
                    Request_QueryString + i + "=" + str(Params[i]) + "&"
                )
    Request_QueryString = Request_QueryString.strip("&")

    # Requst的Header拼接
    Request_Headers = (
        "\nX-Gw-AccessId:"
        + AKID
        + "\nX-Gw-Nonce:"
        + str(UUID)
        + "\nX-Gw-Timestamp:"
        + str(timestamp)
    )

    # 待签名字符串
    StringToSign = Method.upper() + "\n" + URI + Request_QueryString + Request_Headers
    print("StringToSign签名字符串:")
    print(StringToSign)
    encodeString = parse.quote(StringToSign, "")
    print("Encode后的签名字符串:", encodeString)
    sign = hash_hmac(AKSecret, encodeString)
    print("sign签名:", sign)
    return sign


# QBI域名
HOST = "http://quickbi.feihe.com"
# 接口路径
Method_URI = "/openapi/v2/works/bloodRelationship"

URL = HOST + Method_URI
# 请求方式 GET POST PUT DELETE
HTTP_METHOD = "GET"

# 请求方式，根据接口不同更换请求方式
JSON = "application/json"
FORM = "application/x-www-form-urlencoded"
contentType = JSON

# json传参
jsonParam = {"worksId": "86d22be3-faef-4db3-967e-b2d705852029"}
# 表单传参
formParams = {
    "worksId": "6082ca98-3e0a-4d47-95bb-eb08ea2b96f0",
}

# 生成签名
# 生成随机数
UUID_STR = str(uuid.uuid1())
# 请求时间戳 UNIX时间戳，13位
time_unix = str(round(time.time() * 1000))
sign = Signature(
    HTTP_METHOD, Method_URI, formParams, AccessID, AccessKey, UUID_STR, time_unix
)

headers = {
    "X-Gw-AccessId": AccessID,
    "X-Gw-Nonce": UUID_STR,
    "X-Gw-Timestamp": time_unix,
    "X-Gw-Signature": sign,
    # 开启调试
    "X-Gw-Debug": "true",
    "Content-Type": contentType,  # JSON
}
# 发起请求
r = requests.request(
    method=HTTP_METHOD, url=URL, headers=headers, params=formParams, json=jsonParam
)

# 拿到接口返回
print("返回结果：" + r.content.decode("utf-8"))
# print("服务端签名信息：" + str(r.headers))
