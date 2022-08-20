"""
前台框架的操作
"""
import app
import time


def menu_register(path: str, icon="", href="", target="_self") -> bool:
    """
    注册菜单

    :param path: 菜单的路径，用 "/" 隔开，
                顶部菜单创建方法： 顶部菜单
                侧边菜单创建方法： 顶部菜单/侧边菜单
                子菜单创建方法： 顶部菜单/侧边菜单/姊姊菜单
    :param icon: 菜单图标，参见 Font Awesome Icons(https://fontawesome.com/), 允许 svg ，建议尺寸 13~18px
    :param href: 菜单指向链接
    :param target: 菜单打开位置，默认为 _self 为嵌入式加载。
    """

    if icon[:4] == "<svg":
        icon = f"\"></i>{icon}<i class=\""
    if path[0] == "/":
        path = path[1:]
    if path[-1] == "/":
        path = path[:-1]

    def menu_creator(m: list, p: str):
        # m 当前对象菜单 p 当前路径，为递归做准备
        pos = p.find("/")
        if pos == -1:
            m.append({
                'title': p,
                'icon': icon,
                'href': href,
                'target': target,
                'child': []
            })
            return True
        else:
            menu_name = p[:pos]
            for mi in m:
                if mi['title'] == menu_name:
                    return menu_creator(mi['child'], p[pos + 1:])
            else:
                return False

    return menu_creator(app.init_api['menuInfo'], path)


def menu_get(path: str) -> dict:
    """
    获取菜单字典，不存在返回空字典。

    :param path: 菜单的路径，用 "/" 隔开
    :return: 字典，菜单数据 title icon href target
    """

    def menu_finder(m: list, p: str):
        # m 当前对象菜单 p 当前路径，为递归做准备
        pos = p.find("/")
        if pos == -1:
            for mi in m:
                if mi['title'] == p:
                    mi['icon'] = mi['icon'].replace('"></i>', "").replace('<i class="', "")
                    return mi
            else:
                return {}
        else:
            menu_name = p[:pos]
            for mi in m:
                if mi['title'] == menu_name:
                    return menu_finder(mi['child'], p[pos + 1:])
            else:
                return {}

    return menu_finder(app.init_api['menuInfo'], path)


def get_init_api() -> dict:
    """获取初始化 api"""
    return app.init_api


def get_website_setting() -> dict:
    """
    获取主题模板渲染的参数。数据库中 website_setting 表中的值，启动时获取。
    """
    return app.website_setting


def set_quickstart_icon(symbol: str, title: str, icon: str, href: str, mode=0):
    """
    添加库快捷功能按钮，就是首页上的快捷入口（首页默认为前8个）

    :param symbol: 用于标识的符号
    :param title: 按钮标题
    :param icon: 按钮图标，支持 svg 图标
    :param href: 按钮打开链接
    :param mode: 打开方式 0--框架标签页打开  1--框架标签页本页切换
    """
    if symbol not in app.quickstart_icon:
        app.quickstart_icon[symbol] = {}
    app.quickstart_icon[symbol]['title'] = title
    if icon[:4] == "<svg":
        app.quickstart_icon[symbol]['icon'] = icon
    else:
        app.quickstart_icon[symbol]['icon'] = f"<i class='{icon}'></i>"

    app.quickstart_icon[symbol]['href'] = href
    app.quickstart_icon[symbol]['mode'] = mode


def set_notice(symbol: str, title: str, content: str, time_: str = None):
    """
    添加或更改公告

    :param symbol: 公告标识
    :param title: 公告标题
    :param content: 公告内容(html)
    :param time_: 公告时间(默认当前时间 xxxx-xx-xx xx:xx)
    """
    if symbol not in app.notice_data:
        app.notice_data[symbol] = {}
    app.notice_data[symbol]['title'] = title
    app.notice_data[symbol]['content'] = content
    if time_ is None:
        time_ = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    app.notice_data[symbol]['time'] = time_


def set_dashboard_div(symbol: str, html: str):
    """
    在仪表盘页面放卡片
    :param symbol: 标识
    :param html: html代码
        - eg:
        <div class="layui-col-md6">
            <div class="layui-card">
                <div class="layui-card-header"><i class="fa fa-credit-card icon icon-blue"></i>快捷入口
                </div>
                <div class="layui-card-body">
                    测试
                </div>
            </div>
        </div>
    """
    if symbol not in app.dashboard_div_dict:
        app.dashboard_div_dict[symbol] = {}
    app.dashboard_div_dict[symbol] = html
