import os

import sqlite3
import traceback

import psutil
import time
import json

import app
import appdev

from flask import request


def _dict_factory(cursor, row):
    """官方文档中用于输出字典查询格式的函数"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


logCon = sqlite3.connect("data/log", check_same_thread=False, timeout=-1)
logCon.row_factory = _dict_factory


def exit():
    """
    退出程序
    """
    while True:
        time.sleep(0.1)
        appdev.console.warning("* Stopped Application by user. PID:", os.environ.copy()['TAB_TOOLBOX_RUN_MAIN_PID'],
                               os.getppid(), os.getpid())
        pid = int(os.environ.copy()['TAB_TOOLBOX_RUN_MAIN_PID'])
        for proc in psutil.process_iter():  # 杀掉父进程（如果是调试模式应该是父父进程）
            if proc.pid == pid:
                proc.kill()
        for proc in psutil.process_iter():  # 如果是调试模式还有一个父进程
            if proc.pid == os.getppid():
                proc.kill()
        for proc in psutil.process_iter():  # 在杀掉自己
            if proc.pid == os.getpid():
                proc.kill()


def reload():
    """
    重新载入
    """
    appdev.console.warning("* Reloaded Application by user. PID:", os.getpid())
    for proc in psutil.process_iter():
        if proc.pid == os.getpid():
            proc.kill()


def log_write(time_: int, level: int, msg: str):
    """
    写一条日志
    :param time_: 时间
    :param level: 等级
    :param msg: 内容
    """
    msg = json.dumps(msg)
    # 转义
    bf = ["'"]
    af = ["''"]
    for i in range(len(bf)):
        msg = msg.replace(bf[i], af[i])
    c = logCon.cursor()
    while True:
        try:
            c.execute(f"""INSERT INTO record (time, level, msg) values ('{time_}', '{level}', '{msg}')""")
            break
        except sqlite3.DatabaseError as e:
            appdev.console.error("数据库执行出错（将在5s后再试），下面是详细信息：")
            appdev.console.error("\n" + exception_detail(e))
            time.sleep(5)

            continue
    c.close()
    logCon.commit()


def log_get_latest(limit: int) -> list:
    """
    获取最新的n条日志
    :param limit: 条数
    :return: 列表，依次从新到旧。[[时间戳(ns), 日志等级, 信息]]
    """
    c = logCon.cursor()
    c.execute(f"SELECT * from record order by time desc limit {limit}")
    logs = []
    for x in c.fetchall():
        logs.append([x['time'], x['level'], json.loads(x['msg'])])
    c.close()
    return logs


def log_get_by_timestamp(start: int, end: int) -> list:
    """
    时间戳获取日志
    :param start: 开始时间戳
    :param end: 结束时间戳
    :return: 数组，依次从新到旧。[[时间戳(ns), 日志等级, 信息]]
    """
    c = logCon.cursor()
    c.execute(f"SELECT * from record where time>={start} and time<={end}")
    logs = []
    for x in c.fetchall():
        logs.append([x['time'], x['level'], json.loads(x['msg'])])
    c.close()
    return logs


def log_level2name(n: int) -> str:
    """
    日志等级到名称

    return {10: "Plain",
            11: "Log",
            12: "Info",
            13: "Debug",
            14: "Success",
            15: "Warning",
            16: "Error"}.get(n, "Plain")

    :param n: 等级代号
    :return: 名称
    """
    return {10: "Plain",
            11: "Log",
            12: "Info",
            13: "Debug",
            14: "Success",
            15: "Warning",
            16: "Error"}.get(n, "Plain")


def get_public_path() -> list:
    """
    返回 公开链接

    正则匹配法

    e.g 添加 get_public_url().append("^/$")
    e.g 删除 get_public_url().remove("^/$")

    :return: 列表
    """
    return app.website_public_path


def get_filemanager_module() -> dict:
    """
    获取文件管理器模块，模块具体可以参考 core/mod_systemfile 文件

    :return: 模块名对应列表
    """
    return app.filemanager_module


def get_filemanager_allow_target() -> dict:
    """
    获取公开允许的文件管理器路径。

    正则匹配法

    e.g 允许 C:\temp 文件夹 支持列目录(list_path)、上传文件(upload_file)、下载文件(download_file)、新建文件夹(create_folder 自定义 target)
    get_filemanager_allow_target()['^C:\temp$'] = ['list_path', 'upload_file', 'download_file', 'create_folder']
    e.g 删除上述规则
    del get_filemanager_allow_target()['^C:\temp$']

    :return: 公开允许的文件管理器路径。
    """
    return app.filemanager_allow_target


def islogin() -> bool:
    """
    判断用户是否已经登录，未设置管理员密码也算登录。
    :return: 是否登录
    """
    return appdev.setting.get("AdminPassword") in (None, "") or \
           request.cookies.get("AdminPassword", "") == appdev.setting.get("AdminPassword")


def exception_detail(e: any) -> str:
    """
    获取更加详细的错误信息。

    :param e: 触发的错误。就是 Exception XXX as error，中的 error 。
    :return: 详细信息字符串
    """
    info = 'str(Exception):\t' + str(Exception)
    info += 'str(e):\t\t' + str(e)
    info += 'repr(e):\t' + repr(e)
    info += 'traceback.format_exc():\n%s' + traceback.format_exc()
    return info
