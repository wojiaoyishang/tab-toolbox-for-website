# -*- coding: utf-8 -*-
"""
Tab Toolbox for Website
By: Yishang & Pikachu

mod_systemfile.py -- 文件管理的模块之一

其余将会调用提供 target 的字符串对应的函数，并传入参数 path(以分隔符结尾) 和 data，
直接返回函数所返回的值 可以看 core.api_route.filemanager_target() 中的定义。
"""
import os
import re
import time
import psutil
import shutil

from flask import send_file, request

from appdev import application

icons = os.listdir("./static/images/icon")  # 所有图标


def _byte2string(size: int):
    """内部方法 把数字转化成容量带单位的字符串"""
    if size < 1024:
        return str(size) + " Byte"
    elif size < 1024 ** 2:
        return str(round(size / 1024, 2)) + " KB"
    elif size < 1024 ** 3:
        return str(round(size / 1024 ** 2, 2)) + " MB"
    elif size < 1024 ** 4:
        return str(round(size / 1024 ** 3, 2)) + " GB"
    elif size < 1024 ** 5:
        return str(round(size / 1024 ** 4, 2)) + " TB"
    else:
        return str(round(size / 1024 ** 5, 2)) + " PB"


def function(path: str, data=None):
    """
    执行地址栏中输入的特定路径

    :param path: 地址栏输入内容(原始内容)
    :param data: 分解好的功能
    :return: 绝对路径(这里可以自定义), 列表数据(定义见下方)
    [
        {
            "thumb": "图标 <img src="" />",
            "filename": "文件名",
            "created": "创建时间",
            "modified": "修改时间",
            "type": "DIR / FILE",
            "typename": "文件类型名",
            "size": "文件大小"
        },
        ...
    ]
    """

    if data == "show_disk":  # 获取磁盘
        disk = []
        for d in psutil.disk_partitions():
            disk.append({
                "thumb": "/static/images/icon/disk.png",
                "filename": d.device,
                "created": "-",
                "modified": "-",
                "type": "DISK",
                "typename": "-",
                "size": "-"
            })
        return {
            "code": 0,
            "path": "function::show_disk",
            "count": 1,
            "data": disk
        }
    elif data == "pikachu":
        return {
            "code": 0,
            "path": "皮卡丘在我心里 φ(>ω<*) ",
            "count": 1,
            "data": [{
                "thumb": "/static/images/icon/pikachu.png",
                "filename": "皮卡丘最可爱",
                "created": "皮卡丘爱你",
                "modified": "以赏最爱小皮卡",
                "type": "PIKACHU",
                "typename": "IS MY GOD",
                "size": "可爱可爱！"
            }]
        }
    else:
        raise BaseException(f"不存在功能 {path} ！")


def list_path(path: str, data=None):
    """
    列出目录文件

    :param path: 目录路径
    :param data: 额外附加数据(此函数的data参数没有规定)
    :return: 绝对路径(这里可以自定义), 列表数据(定义见下方)
    [
        {
            "thumb": "图标 <img src="" />",
            "filename": "文件名",
            "created": "创建时间",
            "modified": "修改时间",
            "type": "DIR / FILE",
            "typename": "文件类型名",
            "size": "文件大小"
        },
        ...
    ]
    """
    abs_path = os.path.abspath(path)
    files = [{
        "thumb": "/static/images/icon/dir.png",
        "filename": "..",
        "created": "-",
        "modified": "-",
        "type": "DIR",
        "typename": "-",
        "size": "-"
    }]
    for f in os.listdir(path):
        full_path = path + f
        type_ = "DIR" if os.path.isdir(full_path) else "FILE"
        typename = "-" if os.path.isdir(full_path) else os.path.splitext(f)[1][1:]
        if os.path.isdir(full_path):
            thumb = "/static/images/icon/dir.png"
        else:
            if typename + ".png" in icons:
                thumb = f"/static/images/icon/{typename}.png"
            else:
                thumb = "/static/images/icon/file.png"

        files.append({
            "thumb": thumb,
            "filename": f,
            "created": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(full_path))),
            "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(full_path))),
            "type": type_,
            "typename": typename,
            "size": _byte2string(os.path.getsize(full_path))
        })

    return {
        "code": 0,
        "path": abs_path.replace("\\", "/"),
        "count": len(files),
        "data": files
    }


def download_file(path: str, data=None):
    """
    下载文件

    :param path: 目标文件所在文件夹
    :param data: 目标文件名，这里的 data 可能是多个文件
    :return: 文件数据
    """
    if not application.islogin() and re.compile(r"""/|\\|:|\*|"|<|>|\||\?""").search(data) is not None:
        return {
            "code": -1,
            "msg": '非管理员不允许使用非法字符 / \ : * " < > | ?'
        }
    if isinstance(data, list):
        if len(data) != 1:
            return {
                "code": -1,
                "msg": "暂不支持多文件下载。"
            }
        else:
            if os.path.exists(path + data[0]) and os.path.isfile(path + data[0]):
                return send_file(path + data[0])
            else:
                raise BaseException("文件不存在或者不是一个文件！")
    if os.path.exists(path + data) and os.path.isfile(path + data):
        return send_file(path + data)
    else:
        raise BaseException("文件不存在或者不是一个文件！")


def delete_file(path: str, data=None):
    """
    删除文件

    :param path: 要删除的文件所在的文件夹
    :param data: 要删除的文件名，这里的 data 可能是多个文件
    :return: bool 是否删除成功
    """
    if not application.islogin() and re.compile(r"""/|\\|:|\*|"|<|>|\||\?""").search(data) is not None:
        return {
            "code": -1,
            "msg": '非管理员不允许使用非法字符 / \ : * " < > | ?'
        }
    if isinstance(data, list):
        # 批量删除
        for filename in data:
            # 安全措施
            if (path + filename)[-3:] == "/.." and os.path.isdir(path + filename):
                raise BaseException(f"存在安全隐患，不允许这样操作！")
            if os.path.isdir(path + filename):  # 文件夹删除
                shutil.rmtree(path + filename)
            else:  # 文件删除
                os.remove(path + filename)
            if os.path.exists(path + filename):
                raise BaseException(f"删除文件(夹) {path + filename} 失败！")
        return True
    else:
        if os.path.exists(path + data):
            os.remove(path + data)
            return {"code": 0, "msg": "删除文件成功！"} if not os.path.exists(path + data) else {"code": -1,
                                                                                                "msg": "删除文件失败！"}
        else:
            raise BaseException("文件不存在！")


def upload_file(path: str, data=None):
    """
    上传文件

    :param path: 保存的目录
    :param data: 预留的参数(此函数的data参数没有规定，被 upload 占用。)
    :return: 成功保存的位置
    """
    path = path.replace('\\', '/')
    path = path + "/" if path[-1] not in ("/", "\\") else path  # 如果结尾不是 "/" 就加一个 "/"
    f = request.files['data']
    f.save(path + f.filename)
    if os.path.exists(path + f.filename):
        return {
            "code": 0,
            "msg": "上传文件成功",
            "data": {
                "src": path + f.filename
            }
        }
    else:
        raise BaseException("上传文件失败")


def create_folder(path: str, data=None):
    """
    自定义方法：创建文件夹

    :param path: 新文件夹所在父文件夹路径
    :param data: 新建文件夹名
    :return: 返回数据
    """
    if not application.islogin() and re.compile(r"""/|\\|:|\*|"|<|>|\||\?""").search(data) is not None:
        return {
            "code": -1,
            "msg": '非管理员不允许使用非法字符 / \ : * " < > | ?'
        }
    if data.strip() == "":
        return {
            "code": -1,
            "msg": '未输入新文件名！'
        }
    if os.path.exists(path + data):
        return {
            "code": -1,
            "msg": "文件夹已存在"
        }
    os.makedirs(path + data)
    if os.path.exists(path + data):
        return {
            "code": 0,
            "msg": "新建文件夹成功！"
        }
    else:
        return {
            "code": -1,
            "msg": "新建文件夹失败！"
        }


def rename(path: str, data=None):
    """
    自定义方法：重命名文件（夹）

    :param path: 新文件（夹）所在父文件夹路径
    :param data: 列表 [原文件（夹）名, 重命名文件（夹）名]
    :return: 返回数据
    """
    if not application.islogin() and (
            re.compile(r"""/|\\|:|\*|"|<|>|\||\?""").search(data[0]) is not None or re.compile(
        r"""/|\\|:|\*|"|<|>|\||\?""").search(data[1])):
        return {
            "code": -1,
            "msg": '非管理员不允许使用非法字符 / \ : * " < > | ?'
        }
    if data[0].strip() == "" or data[1].strip() == "":
        return {
            "code": -1,
            "msg": '未输入重命名文件！'
        }
    if not os.path.exists(path + data[0]):
        return {
            "code": -1,
            "msg": "文件（夹）不存在！"
        }
    os.rename(path + data[0], path + data[1])
    if not os.path.exists(path + data[0]) and os.path.exists(path + data[1]):
        return {
            "code": 0,
            "msg": "重命名文件（夹）成功！"
        }
    else:
        return {
            "code": -1,
            "msg": "重命名文件（夹）失败！"
        }
