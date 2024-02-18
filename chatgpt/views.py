from django.shortcuts import render

# Create your views here.
from flask import Flask, render_template, request, send_file, redirect, url_for, session
import requests
import threading
import concurrent.futures
import mistune
from datetime import datetime
from functools import wraps
from config import mysql_connect, API_KEY, users, sk

app = Flask(__name__)
app.secret_key = sk  # 设置一个密钥用于会话管理

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
PROXY_URL = "http://127.0.0.1:8001"

proxies = {"http": PROXY_URL, "https": PROXY_URL}

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
# 全局变量，用于存储ChatGPT的回复
completion = {}
event = threading.Event()

completion_lock = threading.Lock()


# 通过api获取回复
def get_gpt_response(chat_id, username):
    global completion

    content_list = c.get_chat_content(chat_id)
    dialogue = [{"role": content[0], "content": content[1]} for content in content_list]

    data = {
        "model": "gpt-3.5-turbo-16k-0613",
        "messages": dialogue,
    }
    try:
        response = requests.post(
            API_ENDPOINT, headers=headers, json=data, proxies=proxies
        )
        output = response.json()
    except Exception as e:
        output = "请求超时，请重新提交"

    if "choices" in output:
        completion_lock.acquire()
        for choice in output["choices"]:
            completion[username] = choice["message"]["content"]
            c.save_chat_detail(chat_id, "assistant", completion[username])
            completion_lock.release()
        return completion
    else:
        return str(output)


# 通过api获取标题
def get_gpt_chatname(username, user_input, chat_id):
    data = {
        "model": "gpt-3.5-turbo-16k-0613",
        "messages": [{"role": "user", "content": "请用3个词概括下面的问题：%s" % user_input}],
    }
    try:
        response = requests.post(
            API_ENDPOINT, headers=headers, json=data, proxies=proxies
        )
        output = response.json()
    except Exception as e:
        output = "请求超时，请重新提交"

    if "choices" in output:
        for choice in output["choices"]:
            chatname = choice["message"]["content"]
            c.save_chat_info(username, chat_id, chatname)
            return chatname
    else:
        return str(output)


class chat_class:
    def get_connect(self):
        return mysql_connect()

    def close_connect(self, cursor, cnx):
        cursor.close()
        cnx.close()

    def init_chat_info(self, username):
        chatname = "New chat"
        chatdate = datetime.now()
        insert_query = "REPLACE INTO chat_history (username, chatname, chatdate) VALUES (%s, %s, %s)"
        values = (username, chatname, chatdate)
        cnx = self.get_connect()
        cursor = cnx.cursor()
        cursor.execute(insert_query, values)
        cnx.commit()

        select_query = (
            "select max(pk_chat_id) from chat_history where username = '%s'"
            % (username)
        )
        cursor.execute(select_query)
        chat_id = cursor.fetchone()[0]
        self.close_connect(cursor, cnx)
        return chat_id

    def save_chat_info(self, username, chat_id, chatname):
        chatdate = datetime.now()
        insert_query = "REPLACE INTO chat_history (pk_chat_id, username, chatname, chatdate) VALUES (%s, %s, %s, %s)"
        values = (chat_id, username, chatname, chatdate)
        cnx = self.get_connect()
        cursor = cnx.cursor()
        cursor.execute(insert_query, values)
        cnx.commit()
        self.close_connect(cursor, cnx)
        return

    def save_chat_detail(self, chat_id, role, content):
        fk_chat_id = chat_id
        role_type = role
        insert_query = "REPLACE INTO chat_history_detail (fk_chat_id, role_type, content) VALUES (%s, %s, %s)"
        values = (fk_chat_id, role_type, content)

        # 执行SQL插入语句
        cnx = self.get_connect()
        cursor = cnx.cursor()
        cursor.execute(insert_query, values)
        cnx.commit()
        self.close_connect(cursor, cnx)
        return

    def get_chat_list(self):
        select_query = (
            "select pk_chat_id,chatname,chatdate from chat_history where username = '%s' order by chatdate desc"
            % (session.get("username"))
        )
        cnx = self.get_connect()
        cursor = cnx.cursor()
        cursor.execute(select_query)
        chat_list = cursor.fetchall()
        self.close_connect(cursor, cnx)
        return chat_list

    def get_chat_content(self, chatid):
        select_query = (
            "select role_type,content from chat_history_detail where fk_chat_id = '%s' order by id"
            % (chatid)
        )
        cnx = self.get_connect()
        cursor = cnx.cursor()
        cursor.execute(select_query)
        content_list = cursor.fetchall()
        self.close_connect(cursor, cnx)
        return content_list


# 定义登录装饰器，用于验证用户登录状态
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "username" not in session or session.get("username") == None:
            return render_template("login.html")
        return func(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("chat"))
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # 在这里编写验证用户名和密码的代码
    # 进行适当的验证逻辑，例如与数据库中的用户进行比较
    if username in users.keys() and password == users[username]:
        # 登录成功，将用户名保存到会话中，初始化聊天信息
        session["username"] = username
        return redirect(url_for("chat"))
    else:
        # 登录失败，返回登录页并显示错误消息
        return render_template("login.html", error_message="用户名或密码不正确")


@app.route("/chat")
@login_required  # 使用登录装饰器验证用户登录状态
def chat():
    return render_template("index.html")


@app.route("/chatpost", methods=["POST"])
def chatpost():
    global completion

    username = session.get("username")
    user_input = request.form["user_input"]
    completion[username] = None

    if "chat_id" not in session or session.get("chat_id") == None:
        chat_id = c.init_chat_info(username)
        session["chat_id"] = chat_id
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(get_gpt_chatname, username, user_input, chat_id)
            session["chat_name"] = future.result()
    else:
        chat_id = session.get("chat_id")

    c.save_chat_detail(chat_id, "user", user_input)
    c.save_chat_info(username, chat_id, session["chat_name"])
    event.clear()
    threading.Thread(
        target=get_gpt_response,
        args=(
            chat_id,
            username,
        ),
    ).start()
    return "正在回复，请稍等..."


@app.route("/get_response", methods=["GET"])
def get_response():
    global completion
    username = session.get("username")
    if completion[username]:
        response = completion[username]
        completion_lock.acquire()
        completion[username] = None
        completion_lock.release()
        event.clear()
        md = mistune.Markdown(renderer=mistune.HTMLRenderer(escape=False))
        html_response = md(response)  # 将Markdown转换为HTML
        return html_response
    else:
        return "还没有回复"


@app.route("/get_chatname", methods=["GET"])
def get_chatname():
    if session.get("chat_name"):
        chatname = session.get("chat_name")
        chatid = session.get("chat_id")
        chatinfo = {"chatname": chatname, "chatid": chatid}
        return chatinfo
    else:
        return "还没有回复"


# @app.route("/export", methods=["GET"])
# def export():
#     with open("dialogue.txt", "w") as file:
#         for line in dialogues:
#             file.write(line + "\n")
#     return send_file("dialogue.txt", as_attachment=True)


@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    chat_list = c.get_chat_list()
    item = [
        {"chatname": chat[1], "chatdate": chat[2], "chatid": chat[0]}
        for chat in chat_list
    ]
    return item


@app.route("/get_chat_content", methods=["POST"])
def get_chat_content():
    chatid = request.form["chatid"]
    chatname = request.form["chatname"]
    session["chat_id"] = chatid
    session["chat_name"] = chatname
    content_list = c.get_chat_content(chatid)

    md = mistune.Markdown(renderer=mistune.HTMLRenderer(escape=False))
    item = [
        {"role_type": content[0], "content": md(content[1])} for content in content_list
    ]
    return item


@app.route("/update_chat_name", methods=["POST"])
def update_chat_name():
    chat_id = session.get("chat_id")
    username = session.get("username")
    new_chat_name = request.form["new_chat_name"]
    c.save_chat_info(username, chat_id, new_chat_name)
    session["chat_name"] = new_chat_name
    return "名称已更新"


@app.route("/reset_session", methods=["GET"])
def reset_session():
    session.pop("chat_id", None)
    session.pop("chat_name", None)
    return "新建会话成功"


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("chat_id", None)
    session.pop("chat_name", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    c = chat_class()
    app.run(host="0.0.0.0")
    # app.run()