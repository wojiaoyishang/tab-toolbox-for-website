import json
import time
import sqlite3
import traceback

import appdev


def _dict_factory(cursor, row):
    """官方文档中用于输出字典查询格式的函数"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# 系统数据库
systemCon = sqlite3.connect("data/system", check_same_thread=False, timeout=-1)
systemCon.row_factory = _dict_factory


def get_setting_data() -> dict:
    """获取数据库中系统的全部设置信息"""
    c = systemCon.cursor()
    c.execute("SELECT * FROM website_setting")
    settings = {}
    for x in c.fetchall():
        settings[x['key']] = json.loads(x['value'])
    c.close()
    return settings


def get_account_data() -> dict:
    """获取数据库中用户账户的全部设置信息"""
    c = systemCon.cursor()
    c.execute("SELECT * FROM account")
    settings = {}
    for x in c.fetchall():
        settings[x['key']] = json.loads(x['value'])
    c.close()
    return settings


def get(key: str, table='system_setting') -> any:
    """
    获得设置

    :argument key: 系统设置键值，默认找到一个，不可能出现多个
    :argument table: 对应表，system_setting -- 系统设置  website_setting -- 网站设置
    :return: 系统设置数据 可能是 str int list dict
    """
    c = systemCon.cursor()
    c.execute(f"""SELECT * FROM {table} WHERE (key) is ('{key}')""")
    result = c.fetchall()
    c.close()
    if len(result) == 0:
        return None
    try:
        return json.loads(result[0]['value'])
    except:
        return None


def set(key: str, value: any, table='system_setting') -> any:
    """
    设置项目.

    :argument key: 系统设置键值，没有则创建。
    :argument value: 值 可以是 int str list dict
    :argument table: 对应表，system_setting -- 系统设置  website_setting -- 网站设置
    """

    value = json.dumps(value)
    # 转义
    bf = ["'"]
    af = ["''"]
    for i in range(len(bf)):
        value = value.replace(bf[i], af[i])
    c = systemCon.cursor()
    while True:
        try:
            c.execute(f"""REPLACE INTO {table} (key, value) values ('{key}', '{value}')""")
            break
        except sqlite3.DatabaseError as e:
            appdev.console.error("数据库执行出错（将在5s后再试），下面是详细信息：")
            appdev.console.error("\n" + appdev.application.exception_detail(e))
            time.sleep(5)
            continue
    c.close()
    systemCon.commit()
