# -*- coding: utf-8 -*-
"""
Tab Toolbox for Website
By: Yishang & Pikachu

main.py -- 使用程序的入口，如果是 flask 开发模式则不会调用这里
"""
import os
import sys
import ctypes
import platform

import config

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-H", "--host", dest="HOST",
                  help="Host for Running", metavar="host")
parser.add_option("-p", "--port", dest="PORT",
                  help="Port for Running", metavar="port")
parser.add_option("-D", "--development", dest="DEVELOPMENT", action="store_true", default=False,
                  help="Development Mode")
parser.add_option("-d", "--debug", dest="DEBUG", action="store_true", default=False,
                  help="Debug Mode")

(options, args) = parser.parse_args()

if options.HOST is None and options.PORT is None and (options.DEVELOPMENT or options.DEBUG):
    print("Missing IP and Port parameters.")
    exit()

# 开启 Windows 下对于 ESC控制符 的支持
if sys.platform == "win32":
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

CONFIG_FILE_CONTENT = """# 注意此文件仅用于配置程序的一些内置内容，比如运行模式、版本号等。按理来讲在发布时此文件已经设定好，不需要更改。

DEVELOPMENT = {DEVELOPMENT}  # 如果更改这个变量那么就会打开开发模式，而不是发布模式
DEBUG = {DEBUG}   # 这个是否为 Debug 模式，主要控制的是 app.run() 中的设置，若是命令行启动则可以忽略
HOST = "{HOST}"  # 设置运行 IP
PORT = {PORT}  # 运行端口
FIRST_RUNNING = False  # 是否第一次运行

TAB_TOOLBOX_VERSION = "{TAB_TOOLBOX_VERSION}"
""".replace("{TAB_TOOLBOX_VERSION}", config.TAB_TOOLBOX_VERSION)

PRINT_CONTENT = "\033[1;34m" + r"""┌┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┐
┆#  _____        _       _____               _  _                  *┆
┆# /__   \ __ _ | |__   /__   \ ___    ___  | || |__    ___ __  __ *┆
┆#   / /\// _` || '_ \    / /\// _ \  / _ \ | || '_ \  / _ \\ \/ / *┆
┆#  / /  | (_| || |_) |  / /  | (_) || (_) || || |_) || (_) |>  <  *┆
┆#  \/    \__,_||_.__/   \/    \___/  \___/ |_||_.__/  \___//_/\_\ *┆ 
┆#                                                                 *┆
├┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┤"""
PRINT_CONTENT = PRINT_CONTENT.replace("#", "\033[1;33m").replace("*", "\033[1;34m")
PRINT_CONTENT += """
┆ \033[1;36m* Tab Toolbox for Website                    * Version: {TAB_TOOLBOX_VERSION}\033[1;34m ┆
┆ \033[1;36m* Official Website: https://lovepikachu.top  * Yishang's Blog.\033[1;34m  ┆
┆ \033[1;36m{Platform}\033[1;34m  ┆
\033[1;34m├┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┤\033[1;34m
┆\033┆ \033[0;32;32m                      Open Source Address                     \033[1;34m  ┆
┆\033[0;32;32m{Github}\033[1;34m ┆
┆\033[0;32;32m{Gitee}\033[1;34m ┆
\033[1;34m└┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘\033[m
""".format(TAB_TOOLBOX_VERSION=config.TAB_TOOLBOX_VERSION,
           Platform=("- Running in Platform: " + platform.platform() + " -").center(62, " "),
           Github="·https://github.com/wojiaoyishang/Tab-Toolbox-for-Website·".center(62, " "),
           Gitee="·https://gitee.com/wojiaoyishang/Tab-Toolbox-for-Website ·".center(62, " "))

if __name__ == "__main__":
    new_environ = os.environ.copy()
    if new_environ.get('TAB_TOOLBOX_RUN_MAIN', 'false') != 'true':
        print(PRINT_CONTENT + "\033[m")
        if options.HOST is None and options.PORT is None:
            try:
                if config.FIRST_RUNNING:
                    print("* 嘿！你好！(￣▽￣)／看来这是你第一次打开此程序，我们需要进行一些配置。当然您也可以使用命令行来运行此程序，更多信息请查看我们的文档！")
                    print("* 总之我们先开始配置吧！\n")
                    host = input("* 首先，此程序运行时\033[0;32;32m绑定的IP地址\033[m 为"
                                 "（默认为 \033[0;32;32m{}\033[m，不用担心输错，您可以在配置文件 config.py 中修改）\nEnter:".format(
                        config.HOST))
                    if host.strip() == "":
                        host = config.HOST
                    config.HOST = host
                    print("* Set HOST to \033[0;32;32m" + host + "\033[m")
                    port = input(
                        "* 其次，要绑定那个\033[0;32;32m端口\033[m呢？（默认为 \033[0;32;32m{}\033[m ）\nEnter:".format(config.PORT))
                    if port.strip() == "":
                        port = config.PORT
                    else:
                        port = int(port)
                    config.PORT = port
                    CONFIG_FILE_CONTENT = CONFIG_FILE_CONTENT.replace("{HOST}", host).replace("{PORT}", str(port))
                    CONFIG_FILE_CONTENT = CONFIG_FILE_CONTENT.replace("{DEBUG}", "False").replace("{DEVELOPMENT}",
                                                                                                  "False")
                    with open("./config.py", "w", encoding='utf-8') as f:
                        f.write(CONFIG_FILE_CONTENT)
                    print("* Set POST to \033[0;32;32m" + str(port) + "\033[m")
                    print("* OK了！现在我们将运行程序，对于调试模式与发布模式的设定请自行修改 config.py 文件！\n")
            except BaseException as e:
                print("* Oh! 出错了！你是不是输入了错误的数据或者是按下了取消组合键？请重试程序再试一次吧！Error:", e)
        else:
            config.HOST = options.HOST
            config.PORT = options.PORT
            config.DEVELOPMENT = options.DEVELOPMENT
            config.DEBUG = options.DEBUG

            CONFIG_FILE_CONTENT = CONFIG_FILE_CONTENT.replace("{HOST}", config.HOST).replace("{PORT}", str(config.PORT))
            CONFIG_FILE_CONTENT = CONFIG_FILE_CONTENT.replace("{DEVELOPMENT}", f"{config.DEVELOPMENT}").replace(
                "{DEBUG}", f"{config.DEBUG}")
            with open("./config.py", "w", encoding='utf-8') as f:
                f.write(CONFIG_FILE_CONTENT)

        print("\033[1;33m{}\033[m\n".format(f" * Running in {config.HOST}:{config.PORT} ... * ".center(64)))
        print("\033[1;33m{}\033[m\n".format(f" * DEVELOPMENT:{config.DEVELOPMENT} DEBUG:{config.DEBUG} * ".center(64)))

    __import__('app').start_flask()
