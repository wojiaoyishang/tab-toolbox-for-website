"""
Hello World 示例插件

By: Yishang & Pikachu
"""
# -*- coding:utf-8 -*-
import os
import random
import importlib

from appdev import ui
from appdev import application
from app import app

from flask import Blueprint, render_template

# 获取插件所在的目录（结尾没有分割符号）
dir_path = os.path.dirname(__file__).replace("\\", "/")
plugin = dir_path[dir_path.rfind("/") + 1:]  # 插件文件夹名称

# 插件允许定义蓝图，不过蓝图的绑定需要自己来，见代码最后注册蓝图的地方
blueprint = Blueprint('helloWorld', __name__, template_folder=dir_path + '/templates', static_folder="static",
                      url_prefix="/helloworld")

# 注册文件管理器模块
application.get_filemanager_module()['hellofile'] = importlib.import_module(f"plugins.{plugin}.hellofile")

# 注册菜单
ui.menu_register("Hello World")
ui.menu_register("Hello World/示例", "fa-solid fa-code", "/helloworld")

# 注册快捷按钮
ui.set_quickstart_icon("helloworld", "你好世界", "fa-solid fa-earth-africa", "/helloworld", 0)

# 添加一则公告
ui.set_notice("helloworld", "来自 Hello World 插件的公告",
              "<p>这个是一条来自 Hello World 测试公告，您可以在 Python 中 from appdev import ui</p>\n"
              "<p>再使用 set_notice(symbol, title, content, [time_]) 来添加！</p>")

# 仪表盘添加卡片
ui.set_dashboard_div("helloworld1", """
        <div class="layui-col-md6">
            <div class="layui-card">
                <div class="layui-card-header"><i class="fa-solid fa-flask-vial icon icon-blue"></i>helloworld插件测试</div>
                <div class="layui-card-body">
                    这个是一条来自 Hello World 测试卡片，您可以在 Python 中 from appdev import ui <br>
                    然后使用 ui.set_dashboard_div(symbol, html) 来添加这一个卡片。  
                </div>
            </div>
        </div>""")
ui.set_dashboard_div("helloworld2", f"""
        <div class="layui-col-md6">
            <div class="layui-card">
                <div class="layui-card-header"><i class="fa-solid fa-flask-vial icon icon-blue"></i>helloworld插件测试</div>
                <div class="layui-card-body">
                    一个插件可以创建多个卡片，而且可以定义不同内容。比如生成随机数，你今天的幸运数字是：{random.randint(10000, 99999)} 
                    <br><br><br>
                </div>
            </div>
        </div>""")


@blueprint.route("/")
def helloworld():
    return render_template("helloworld.html")


# 等完全加载过一遍代码后，再调用app.py文件中的app注册蓝图函数注册蓝图
app.register_blueprint(blueprint)
