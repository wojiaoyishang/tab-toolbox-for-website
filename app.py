# -*- coding: utf-8 -*-
"""
Tab Toolbox for Website
By: Yishang & Pikachu

app.py -- flask 启动的文件，这里是 Tab Toolbox for Website 的主入口
"""
import re

import importlib
import reloading
import time

from config import *

from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

import appdev.setting as setting
import appdev.ui as ui
import appdev.plugin as plugin
import appdev.console as console
from core import api_route as core_api_route
from core import page_route as core_page_route

# 这里开始计时
environ = reloading.new_environ  # 主要是防止 PyCharm 把 import reloading 标黑
beginning_run = time.time()

# 定义程序运行时的变量

app = Flask(__name__, template_folder="templates", static_folder="static")  # flask 的 app
app.logger = None
http_server = WSGIServer((HOST, PORT), app, log=None)


def start_flask():
    """这是是给非调试模式(flask启动)使用的启动函数，被 main.py 和 此脚本最后 调用"""
    if DEVELOPMENT:
        app.run(HOST, PORT, debug=DEBUG)
    else:
        http_server.serve_forever()


# 允许访客访问的页面
website_public_path = ["^/favicon.ico$", "^/login$", "^/static/(.*)$", "^/api/verifyAdminPassword$", "^/filemanager$",
                       "^/api/filemanager$"]

# 文件管理载入的模块
filemanager_module = {"systemfile": importlib.import_module("core.mod_systemfile")}

# 未验证管理员密码时，文件管理器 target功能 设置
filemanager_allow_target = {"D:/$": ['list_path', 'create_folder']}

# 网页变量
website_setting = {}  # 网站设置变量

# 载入数据库中的设置
website_setting.update(setting.get_setting_data())

# 适配新版本 设置主页地址
if "index_path" not in website_setting:
    console.log("更新设置：主页地址（已添加 index_path 到 website_setting）")
    setting.set("index_path", "/", "website_setting")
    website_setting['index_path'] = "/"

# 适配新版本 公开地址
if "public_path" not in website_setting:
    console.log("更新设置：主页地址（已添加 public_path 到 website_setting）")
    setting.set("public_path", "", "website_setting")
    website_setting['public_path'] = ""

website_public_path.extend(website_setting['public_path'].split("\n"))  # 更新数据库中定义的白名单链接

# 后台全局设置变量
init_api = {
    "homeInfo": {
        "title": "首页",
        "href": "/dashboard"
    },
    "logoInfo": {
        "title": website_setting['website_logo_title'],
        "image": website_setting['website_logo'],
        "href": ""
    },
    "menuInfo": [
    ]
}

# 快捷入口设置
quickstart_icon = {}

# 公告设置
notice_data = {}

# 主页小工具
dashboard_div_dict = {}

# ------初始化程序------

# 注册菜单
ui.menu_register("程序首页")
ui.menu_register("程序首页/仪表盘", "fa-solid fa-house", "/dashboard")
ui.menu_register("程序首页/插件", "fa-brands fa-atlassian")
ui.menu_register("程序首页/插件/管理插件", "fa-solid fa-list", "/plugin/list")
ui.menu_register("程序首页/快捷入口", "fa-solid fa-rocket", "/quickstart")
ui.menu_register("程序首页/文件管理 ", "fa-solid fa-folder", "/filemanager")
ui.menu_register("程序首页/日志查看", "fa-solid fa-newspaper", "/log")
ui.menu_register("程序首页/程序设置", "fa-solid fa-circle-user", "/setting")
ui.menu_register("程序首页/关于", "fa-solid fa-book", "/about")

# 导入程序核心蓝图
app.register_blueprint(core_api_route.blueprint)  # 核心 api 请求接口
app.register_blueprint(core_page_route.blueprint)  # 核心 页面 请求接口

# 载入插件过程
plugin.plugin_load()


# 绑定主页框架页面
@app.route(website_setting['index_path'])
def index_page():
    return render_template('core-index.html', **ui.get_website_setting(), account=setting.get_account_data())


# 非管理员限制
@app.before_request
def verify():
    # 获取真实 IP 地址并更改 flask 原有的 IP 地址 (注意：只有最新版 flask 才能更改)
    if 'HTTP_X_FORWARDED_FOR' in request.headers:
        arr = request.headers['HTTP_X_FORWARDED_FOR'].strip().split(",")
        i = 0
        while i < len(arr):
            if arr[i].find("unknown") != -1:
                del arr[i]
            else:
                i += 1
        if len(arr) != 0:
            request.remote_addr = arr[0].strip()
    elif 'HTTP_CLIENT_IP' in request.headers:
        request.remote_addr = request.headers['HTTP_CLIENT_IP']
    elif 'REMOTE_ADDR' in request.headers:
        request.remote_addr = request.headers['REMOTE_ADDR']
    elif 'X-Forwarded-For' in request.headers:
        request.remote_addr = request.headers['X-Forwarded-For']

    if setting.get("AdminPassword") in (None, "") or request.cookies.get("AdminPassword", "") == setting.get(
            "AdminPassword"):
        return
    else:
        for path in website_public_path:
            if path.strip() == "":  # 不允许空白
                continue
            if re.match(path, request.path):
                return
        console.info(request.remote_addr, "--", f"访问连接 {request.full_path} 被拒，原因：没有验证管理员密码！")
        return f"<script>window.location.href='/login?referer={request.full_path}'</script>"  # JavaScript 脚本跳转方式


# 提示一下。
console.log(f"初始化完毕！初始化耗费时间：{round(time.time() - beginning_run, 2)}s。加载插件数量：{len(plugin.plugins_pointer)}。")

if __name__ == "__main__":
    start_flask()
