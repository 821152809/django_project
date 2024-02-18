import pymysql

# 数据库连接信息
db_config = {
    'user':'root',
    'password':'123456',
    'host':'127.0.0.1',
    'database':'chatgpt'
}
API_KEY = "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"
sk = 'b859bdc8f0a91783d6dc0414d9c2c34c'  # 设置一个密钥用于会话管理
users = {
    "admin":"admin",
    "guopengcheng":"guopengcheng",
    "chenli":"chenli",
    "liuyinya":"liuyinya"
}

# 连接到MySQL数据库
def mysql_connect():
    return pymysql.connect(**db_config)
