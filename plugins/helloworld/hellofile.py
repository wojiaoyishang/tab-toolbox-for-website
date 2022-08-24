"""
文件管理模块示例
"""
import random
import os

typenames = ['txt', 'zip', 'rar', 'ppt', 'mp3', 'mp4', 'html', 'png', 'jpg']

icons = os.listdir("./static/images/icon")  # 所有图标


def function(path: str, data=None):
    r = []
    for x in range(10):
        typename = random.choice(typenames)
        if typename + ".png" in icons:
            thumb = f"/static/images/icon/{typename}.png"
        else:
            thumb = "/static/images/icon/file.png"
        r.append({
            "thumb": thumb,
            "filename": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5),
            "created": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5),
            "modified": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5),
            "type": random.choice(['DIR', 'FILE']),
            "typename": typename,
            "size": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5)
        })

    return {
        "code": 0,
        "path": path,
        "count": len(r),
        "data": r
    }


def list_path(path: str, data=None):
    r = []
    for x in range(10):
        typename = random.choice(typenames)
        if typename + ".png" in icons:
            thumb = f"/static/images/icon/{typename}.png"
        else:
            thumb = "/static/images/icon/file.png"
        r.append({
            "thumb": thumb,
            "filename": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5),
            "created": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5),
            "modified": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5),
            "type": random.choice(['DIR', 'FILE']),
            "typename": typename,
            "size": random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXY', 5)
        })

    return {
        "code": 0,
        "path": path,
        "count": len(r),
        "data": r
    }


def download_file(path: str, data=None):
    ...
    return "下载文件的内容"


def delete_file(path: str, data=None):
    ...
    return {
        "code": 0,
        "msg": "失败"
    }  # 是否成功 （失败 code 为 非0）


def upload_file(path: str, data=None):
    ...
    return {
        "code": 0,
        "msg": "上传文件成功",
        "data": {
            "src": "保存的地方"
        }
    }
