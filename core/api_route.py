# -*- coding: utf-8 -*-
"""
Tab Toolbox for Website
By: Yishang & Pikachu

api_route.py -- Tab Toolbox for Website 的 API 接口文件。
"""
import re

from flask import Blueprint, request, make_response
from markupsafe import escape

import app
import appdev.ui
import appdev.setting
import appdev.plugin
import appdev.application
import appdev.console

import os
import json
import shutil
import hashlib

import requests
from bs4 import BeautifulSoup

from appdev import setting

blueprint = Blueprint('core_api_route', __name__)


def _log(*args):
    """用于便于输出"""
    app.console.log(request.remote_addr, "--", *args)


def _success(*args):
    """用于便于输出"""
    app.console.success(request.remote_addr, "--", *args)


def _error(*args):
    """用于便于输出"""
    app.console.error(request.remote_addr, "--", *args)


@blueprint.route("/api/init")
def init():
    """首页配置api"""
    return appdev.ui.get_init_api()


@blueprint.route("/api/plugin/get")
def plugin_get():
    """获取插件"""
    try:
        plugins_info = []
        try:
            page = int(request.args.get('page'))  # 页数
            limit = int(request.args.get('limit'))  # 页面元素个数
            search_params = json.loads(request.args.get('search_params'))
            _log(f"使用 page={page} limit={limit} search_params={search_params} 查询了插件。")
        except BaseException as e:
            _log("默认使用 page=1 limit=15 search_params=None 查询了插件。 Except:", e)
            page = 1
            limit = 15
            search_params = None
        i = 0  # 用于计数
        for plugin in app.plugin.get_exist():  # 罗列有效插件
            plugin_path = "plugins/" + plugin
            with open(plugin_path + "/plugin.json", 'r', encoding='utf-8') as f:
                # 读取全部数据
                info = json.loads(f.read())
                # 把路径也写进去
                info['PLUGIN'] = plugin
                # 写是否启用
                if plugin_path in appdev.plugin.plugins_pointer.keys():
                    info['ENABLE'] = "√"
                else:
                    info['ENABLE'] = "×"
                # 搜索插件
                if search_params is not None:
                    if info['PLUGIN_NAME'].lower().find(search_params['pluginName'].lower()) != -1:
                        if (page - 1) * limit <= i < page * limit:
                            if i > page * limit:
                                break
                            plugins_info.append(info)
                            i += 1
                else:
                    if i > page * limit:
                        break
                    plugins_info.append(info)
                    i += 1
    except BaseException as error:
        return {
            "code": -1,
            "msg": "error:" + str(error)
        }
    return {
        "code": 0,
        "msg": "成功。",
        "count": len(plugins_info),
        "data": plugins_info
    }


@blueprint.route('/api/plugin', methods=['POST'])
def plugin_target():
    """插件的操作"""
    target = escape(request.form.get('target', None))  # 操作行为
    plugin = escape(request.form.get('plugin', None))  # 插件路径
    if target is None or plugin is None:
        _log(f"尝试操作插件被拒，未提供操作({target})或者插件({plugin})")
        return {
            "code": -1
        }
    _log(f"尝试操作({target})插件:" + plugin)
    if target == "EnableOrDisable":  # 禁用或启用插件
        if plugin in appdev.plugin.get_enable():
            if appdev.plugin.disable(plugin):
                _success(f"尝试禁用插件({plugin})成功，等待服务器重启。")
                appdev.application.reload()
            else:
                _error(f"尝试禁用插件({plugin})失败。")
                return {
                    "code": -1,
                    "msg": "disable failed."
                }
        else:
            if appdev.plugin.enable(plugin):
                _success(f"尝试启用插件({plugin})成功，等待服务器重启。")
                appdev.application.reload()
            else:
                _error(f"尝试启用插件({plugin})失败。")
                return {
                    "code": -1,
                    "msg": "enable failed."
                }
    elif target == "Delete":  # 删除插件
        _success(f"尝试请求删除插件({plugin})成功，等待服务器删除并重启。")
        appdev.plugin.disable(plugin)
        shutil.rmtree(os.path.abspath("./plugins/" + plugin))
        appdev.application.reload()

    return {
        "code": 0
    }


@blueprint.route('/api/setting/account', methods=['POST', 'GET'])
def setting_account():
    """账户操作"""
    target = escape(request.form.get('target', request.args.get('target', None)))  # 操作行为
    if target == "logout":  # 登出请求
        _log("用户提交登出请求。")
        appdev.setting.set("isLogin", False, table='account')  # 设置用户未登录
        _log("用户成功登出。")
        return {
            "code": 0,
            "msg": "成功登出！"
        }
    elif target == "local.change_username":  # 改变本地用户名，只有一种可能：设置本地用户登录时
        username = escape(request.form['username'])  # 提交的用户名
        nickname = escape(request.form['nickname'])  # 提交的昵称
        description = escape(request.form['description'])  # 提交的介绍
        _log("用户提交本地登录请求(local.change_username)", username, nickname, description)
        if username.strip() == "" or nickname.strip() == "" or description.strip() == "":
            _error("失败：用户名、昵称或介绍为空。")
            return {
                "code": -1,
                "msg": "用户名、昵称或介绍为空！"
            }
        appdev.setting.set("isLogin", True, table='account')  # 设置用户已经登录
        appdev.setting.set("username", username, table='account')  # 设置用户名
        appdev.setting.set("nickname", nickname, table='account')  # 设置昵称
        appdev.setting.set("description", description, table='account')  # 设置介绍
        appdev.setting.set("avatar", "/static/images/avatar.jpg", table='account')  # 设置头像，哈哈哈这里已经给我写死了，谁都不准改我的皮卡丘！
        _success("成功：已设置本地登录。")
        return {
            "code": 0,
            "msg": "成功设置本地登录！"
        }
    elif target == "cloud.login_ysdmmxw":  # 登录云端(以赏的秘密小屋)
        try:
            _log("用户提交云端(以赏的秘密小屋)登录请求(cloud.login_ysdmmxw)")
            cookie = request.args['cookie']  # 提交的 cookie
            # 《我爬我自己的博客》
            # 构建请求头部分内容
            headers = {
                'cookie': cookie,
            }

            response = requests.get("https://lovepikachu.top/me/settings", headers=headers)
            if len(response.content) == 0:
                _error("失败：callback 的 cookie 无效")
                return "<script>alert('获取cookie时发现，cookie无效！');window.close()</script>"

            html = BeautifulSoup(response.content.decode(), 'lxml')
            nickname = html.find("input", attrs={"name": "nickname"}).attrs['value']
            description = html.find("textarea", attrs={"name": "description"}).text
            username = html.find("input", attrs={"name": "user_email"}).attrs['value']  # 把邮箱作为用户名
            avatar = html.find("label", attrs={"title": "上传头像"}).find("img").attrs['src']

            with open("./static/images/avatar_cloud.jpg", "wb") as f:
                f.write(requests.get(avatar).content)  # 下载头像

            appdev.setting.set("avatar", "/static/images/avatar_cloud.jpg", table='account')  # 设置为云端的图片
            appdev.setting.set("isLogin", True, table='account')  # 设置用户已经登录
            appdev.setting.set("username", username, table='account')  # 设置用户名
            appdev.setting.set("nickname", nickname, table='account')  # 设置昵称
            appdev.setting.set("description", description, table='account')  # 设置介绍
            appdev.setting.set("isCloud", True, table='account')  # 云端登录
            appdev.setting.set("cloud.type", "ysdmmxw", table='account')  # 云端类型
            appdev.setting.set("cloud.cookie", cookie, table='account')  # 云端cookie

            _success("成功：已获取用户名基本信息。", username, nickname, description)
            return "<script>alert('登录成功！请刷新 Tab Toolbox for Website 页面查看登录情况！');window.close()</script>"
        except BaseException as e:
            _error("失败：处理数据时出错")
            return {
                "code": -1,
                "msg": "服务器错误。" + str(e)
            }

    return {
        "code": -1,
        "msg": "错误请求"
    }


@blueprint.route("/api/setting/setAdminPassword", methods=['POST'])
def setting_set_admin_password():
    """设置管理密码"""
    password = request.form.get("password", "")
    if password.strip() == "":
        password = ""
    else:
        password = hashlib.sha1((password + "PIKACHUILOVEYOU").encode()).hexdigest()  # 哈希加盐
    appdev.setting.set("AdminPassword", password, "system_setting")
    _success("设置管理员密码成功")
    return {
        "code": 0,
        "msg": "设置管理员密码成功"
    }


@blueprint.route("/api/setting/website", methods=["POST"])
def setting_website():
    """网站设置"""
    try:
        website_title = escape(request.form['website_title'])
        website_icon = escape(request.form['website_icon'])
        website_logo_title = escape(request.form['website_logo_title'])
        website_logo = escape(request.form['website_logo'])
        website_keywords = escape(request.form['website_keywords'])
        website_description = escape(request.form['website_description'])
        index_path = escape(request.form['index_path'])
    except BaseException as e:
        _error("没有填全设置信息", e)
        return {
            "code": -1,
            "msg": "至少有一项没有填全！"
        }

    try:
        public_path = str(escape(request.form.get("public_path", "")))

        # 修改数据库
        appdev.setting.set("website_title", website_title, "website_setting")
        appdev.setting.set("website_icon", website_icon, "website_setting")
        appdev.setting.set("website_logo_title", website_logo_title, "website_setting")
        appdev.setting.set("website_logo", website_logo, "website_setting")
        appdev.setting.set("website_keywords", website_keywords, "website_setting")
        appdev.setting.set("website_description", website_description, "website_setting")
        appdev.setting.set("index_path", index_path, "website_setting")
        appdev.setting.set("public_path", public_path, "website_setting")

        # 一开始运行时修改读取的数据
        app.website_setting['website_title'] = website_title
        app.website_setting['website_icon'] = website_icon
        app.website_setting['website_logo_title'] = website_logo_title
        app.website_setting['website_logo'] = website_logo
        app.website_setting['website_keywords'] = website_keywords
        app.website_setting['website_description'] = website_description
        app.website_setting['index_path'] = index_path
        app.website_public_path.extend(public_path.split("\n"))

        _success("成功设置 public_path(链接白名单) 程序运行时的链接白名单为", app.website_public_path)
    except BaseException as e:
        _error("出现错误 Except:", e)
        return {
            "code": -1,
            "msg": str(e)
        }

    _success("成功修改配置，部分配置重启工具箱生效！")
    return {
        "code": 0,
        "msg": "成功修改配置，部分配置重启工具箱生效！"
    }


@blueprint.route("/api/setting/config", methods=["POST"])
def setting_config():
    """绑定IP设置"""
    try:
        host = escape(request.form['host'])
        port = escape(request.form['port'])
        development = escape(request.form.get('development', 'false'))
        debug = escape(request.form.get('debug', 'false'))
    except BaseException as e:
        _error("没有填全设置信息", e)
        return {
            "code": -1,
            "msg": "至少有一项没有填全！"
        }

    development = 'True' if development == 'true' else 'False'
    debug = 'True' if debug == 'true' else 'False'

    config_file = "# 注意此文件仅用于配置程序的一些内置内容，比如运行模式、版本号等。按理来讲在发布时此文件已经设定好，不需要更改。\n\n"
    config_file += f"DEVELOPMENT = {development}  # 如果更改这个变量那么就会打开开发模式，而不是发布模式\n"
    config_file += f"DEBUG = {debug}   # 这个是否为 Debug 模式，主要控制的是 app.run() 中的设置，若是命令行启动则可以忽略\n"
    config_file += f"""HOST = "{host}"  # 设置运行 IP\n"""
    config_file += f"PORT = {port}  # 运行端口\n"
    config_file += "FIRST_RUNNING = False  # 是否第一次运行\n\n\n"
    config_file += f"""TAB_TOOLBOX_VERSION = "{app.TAB_TOOLBOX_VERSION}" """

    with open("config.py", "w", encoding="utf-8") as f:
        f.write(config_file)

    return {
        "code": 0,
        "msg": "成功写入配置文件，重启工具箱后请使用设置的地址访问！"
    }


@blueprint.route("/api/verifyAdminPassword", methods=['POST'])
def verify_admin_password():
    """
验证管理员密码
"""
    password = request.form.get("password", "")
    password = hashlib.sha1((password + "PIKACHUILOVEYOU").encode()).hexdigest()  # 哈希加盐

    if password == appdev.setting.get("AdminPassword", "system_setting"):
        _success("验证管理员密码成功。")
        resp = make_response({"code": 0, "msg": "验证成功"})
        resp.set_cookie('AdminPassword', password, max_age=3600 * 24 * 100)
        return resp
    else:
        _error("验证管理员密码失败。")
        return {
            "code": -1,
            "msg": "验证失败"
        }


@blueprint.route("/api/process", methods=['POST'])
def process_target():
    """
    对工具箱进程的操作
    """
    target = escape(request.form.get('target', request.args.get('target', None)))  # 操作行为
    if target == "reload":  # 重启
        _log("接到重启操作。")
        appdev.application.reload()
    elif target == "exit":  # 关闭
        _log("接到关闭操作。")
        appdev.application.exit()
    _error("接到未知操作！")
    # 要么重启要么关闭，这里只有随便请求才看得见
    return {
        "code": -1,
        "msg": "error"
    }


@blueprint.route("/api/filemanager", methods=['GET', 'POST'])
def filemanager_target():
    """
    文件管理器
    """
    module = escape(request.form.get("module", request.args.get("module", "null")))
    target = escape(request.form.get("target", request.args.get("target", "null")))
    path = request.form.get("path", request.args.get("path", "null"))
    data = request.form.get("data", request.args.get("data", "null"))

    if module not in appdev.application.get_filemanager_module() or path == "null" or path.strip() == "":
        return {
            "code": -1,
            "msg": "未提供正确的参数。"
        }
    try:
        # 解码 json 数据
        path = json.loads(path)
        data = json.loads(data)

        if target != "function":
            path = path.replace('\\', '/')
            path = path + "/" if path[-1] not in ("/", "\\") else path  # 如果结尾不是 "/" 就加一个 "/"

        # 用户不是管理员则判断权限
        if not appdev.application.islogin():
            filemanager_allow_target = appdev.application.get_filemanager_allow_target()
            for p in list(filemanager_allow_target.keys()):
                if re.match("^" + p, path):
                    break
            else:
                raise BaseException("不允许访问的路径！")
            if target not in filemanager_allow_target[p]:
                raise BaseException("不允许执行的方法！")

        return getattr(app.filemanager_module[module], target)(path, data)
    except AttributeError as e:
        return {
            "code": -1,
            "msg": f"模块 {module} 未定义的方法名 {target}<br>Except:" + str(e)
        }
    except BaseException as e:
        return {
            "code": -1,
            "msg": str(e)
        }
