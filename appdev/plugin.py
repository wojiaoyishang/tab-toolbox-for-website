import os
import importlib

import appdev.setting as setting
import appdev.console as console

plugins_pointer = {}  # 插件指针 {plugin:point}


def plugin_load():
    """
    载入插件，载入插件会重新将 plugins_pointer 变量赋值。
    """
    global plugins_pointer
    plugins_pointer = {}
    enable_plugins = get_enable()

    for file in get_exist():
        try:
            if file in enable_plugins:
                plugins_pointer["plugins/" + file] = importlib.import_module("plugins." + file)
                console.success("Load Plugin Success:", file)
        except BaseException as error:
            console.error("Failed to load Plugin:", str(error))


def get_enable() -> list:
    """
    获取数据库中启用的插件，返回的是数据库中启用了插件。如果想要查看程序加载插件的数量请用 len(plugin.plugins_pointer) 统计
    （注意：这里的列表各个项为 plugins 文件夹中的各插件文件夹名）

    :return: 一个包含启用的插件列表
    """
    p = setting.get('enable_plugins')
    if p is None:
        p = []
    return p


def get_exist() -> list:
    """
    获取在 plugin 文件夹中有效插件。
    （注意：这里的列表各个项为 plugins 文件夹中的各插件文件夹名）

    :return: 插件列表
    """
    r = []
    for file in os.listdir("plugins"):
        if os.path.isdir("plugins/" + file):
            if os.path.exists("plugins/" + file + "/plugin.json"):
                r.append(file)
    return r


def disable(plugin: str) -> bool:
    """
    进行禁用插件
    （注意：这里的列表各个项为 plugins 文件夹中的各插件文件夹名）

    :arg plugin e.g 你好世界
    :return 是已经启用且成功删除数据库中的启用设置返回 True，反之亦然
    """
    all_plugin = get_enable()
    try:
        all_plugin.remove(plugin)
        setting.set("enable_plugins", all_plugin)
        return True
    except:
        return False


def enable(plugin: str) -> bool:
    """
    进行启用插件
    （注意：这里的列表各个项为 plugins 文件夹中的各插件文件夹名）

    :arg plugin e.g 你好世界
    :return 存在、未启用且成功设置数据库中的启用设置返回 True，反之亦然
    """
    enable_plugins = get_enable()
    if plugin not in get_exist():
        return False
    if plugin in enable_plugins:
        return False
    try:
        enable_plugins.append(plugin)
        setting.set("enable_plugins", enable_plugins)
        return True
    except:
        return False
