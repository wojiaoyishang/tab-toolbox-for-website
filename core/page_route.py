from flask import Blueprint, render_template, request, redirect
from markupsafe import escape

import app
import time
from appdev import ui, setting, application

blueprint = Blueprint('core_page_route', __name__)


@blueprint.route('/favicon.ico')
def favicon():
    """为浏览器增加图标支持"""
    return redirect(app.website_setting['website_icon'])


@blueprint.route('/dashboard')
def dashboard_page():
    logs = application.log_get_latest(10)  # 展示最新的10条日志
    logs.reverse()
    for log in logs:
        log[0] = int(log[0])
        log[1] = application.log_level2name(int(log[1]))
        log[0] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(log[0] / 1000000000))

    shortcut = list(app.shortcut_icon.values())[:8]
    while len(shortcut) < 8:
        shortcut.append({"title": "未添加", "icon": "<i class='fa-solid fa-ban'></i>", "mode": 0, "href": ""})

    return render_template('core-dashboard.html',
                           **ui.get_website_setting(),
                           shortcut_icon=shortcut,
                           notice_data=app.notice_data,
                           TAB_TOOLBOX_VERSION=app.TAB_TOOLBOX_VERSION,
                           dashboard_div_dict=app.dashboard_div_dict,
                           account=setting.get_account_data(),
                           latest_logs=logs)


@blueprint.route('/about')
def about_page():
    return render_template('core-about.html', **ui.get_website_setting())


@blueprint.route('/plugin/list')
def plugin_page():
    return render_template('core-plugin.html', **ui.get_website_setting())


@blueprint.route('/setting')
def setting_page():
    return render_template('core-setting.html', **ui.get_website_setting(), account=setting.get_account_data(),
                           host=app.HOST, port=app.PORT, development=app.DEVELOPMENT, debug=app.DEBUG)


@blueprint.route('/shortcut')
def shortcut_page():
    return render_template('core-shortcut.html', **ui.get_website_setting(), shortcut_icon=app.shortcut_icon)


@blueprint.route('/log')
def log_page():
    start = request.args.get("start")
    end = request.args.get("end")
    if start is None:
        start = str(int(time.time() - 60 * 60 * 24 * 30) * 1000)  # 30天的日志
    if end is None:
        end = str(int(time.time() * 1000))
    logs = application.log_get_by_timestamp(int(escape(start)) * 1000000,
                                            int(escape(end)) * 1000000)

    for log in logs:
        log[0] = int(log[0])
        log[1] = application.log_level2name(int(log[1]))
        log[0] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(log[0] / 1000000000))

    return render_template('core-log.html', **ui.get_website_setting(), shortcut_icon=app.shortcut_icon,
                           latest_logs=logs)


@blueprint.route('/login')
def login_page():
    return render_template("core-login.html")


@blueprint.route('/filemanager')
def filemanage_page():
    return render_template("core-filemanager.html", **ui.get_website_setting())
