<p align="center">
  <a href="https://layui.github.io/">
    <img src="https://wojiaoyishang.gitee.io/tab-toolbox-for-website-document/_images/index_logo.png" width="100">
  </a>
    <h1 align="center">Tab Toolbox for Website</h1>
    <p align="center">
      基于 Python 的一款在线工具箱
    </p>
</p>

---

Tab Toolbox for Website 基于 Python 构建，采用了 layuimini 的管理后台模板，提供更加方便的代码设计。并将 layuimini 的代码进行更改，采用最新的 layui 前端UI框架进行设计。

Tab Toolbox for Website 最开始是 Windows 平台 中的 Tab 工具箱 一个程序，
由鑫凯提出并创立制作，后来由以赏加入制作。Tab 工具箱宗旨是为用户使用电脑时解决不便，

Tab Toolbox for Website 则是以赏在此宗旨上用 Python 重建。采用 B/S 架构，支持一台设备安装多台设备使用。

Tab Toolbox for Website 是操作系统上的一个实用小工具，拥有灵活的插件功能，高自由度的插件自定义功能，与高中信息技术接轨，任何人员均可以使用 Python 自由的添加功能。

大部分自带的插件均为 以赏 和 鑫凯 提供，

后续 Tab Toolbox for Website 将会散发出更多的活力！

## 更新日志

### 1.5.0.0 (2022.8.20)

- [~] 修正了 插件操作api 请求时可能出现的错误
- [~] 修改了 部分代码 的语法问题
- [~] 优化了 JavaScript 的部分代码
- [~] 修复了 退出 函数没有解决子进程的问题
- [~] 修复 控制台输出 对 其它类型数据 的支持
- [~] 重写了重新 获取远程地址 的算法
- [~] 修改账户 设置页面 为 系统设置 页面
- [~] 修改了 系统设置页面 的排版
- [~] 修复了 正则表达式 匹配的安全隐患
- [~] 修改了 css 样式为 easyadmin（同 layuimini 作者的另一个开源项目）
- [+] 优化了 appdev 模块引用导致循环导入的问题
- [+] 采用了 layui 2.7.6 组件库
- [+] 支持了 设置 的修改
- [+] 增加了对 框架主页地址 的修改
- [+] 增加了对 工具箱进程 的操作
- [+] 增加了 文件管理 功能与组件，方便插件调用
- [+] 增加了 示例插件 Hello World 的新版功能
- [+] 增加了 吐司提示（来源于开源项目 Pear Admin ）
- [+] 增加了 皮卡丘 喜欢的设定

## 快速开始

### 克隆仓库

```$ git clone git@github.com:wojiaoyishang/Tab-Toolbox-for-Website.git```

### 安装 Python 运行环境

克隆仓库完成之后，您需要检查您的电脑中是否存在 Python 环境，因为程序基于 Python 运行。请注意您的 Python 版本必须在 3.8.0 及以上，3.7.X 的 Python 版本并未进行测试。

Python 的安装地址可以前往 Python 官网下载，链接在这里：https://www.python.org/downloads/release/python-380/

### 安装 Python 的模块

在确认 Python 的环境准确无误后，请确认 Python 中所支持的模块是否安装。对于 Tab Toolbox for Website 运行必要的模块在 仓库根目录下的 requirements.txt 中。内容如下：

运行的第三方库

```text
bs4==0.0.1
Flask==2.1.3
gevent==20.6.2
MarkupSafe==2.1.1
pandas==1.4.3
psutil==5.7.2
requests==2.24.0
lxml==4.5.2
```

可以使用 pip 进行安装，如下：

快速安装库 方法一
```$ pip install -r requirements.txt```
或者您可以试试，

快速安装库 方法二
```$ python -m pip install -r requirements.txt```

在确保准确无误安装好 Python 以及其 模块 后，可以进行运行测试。使用 Python 启动 main.py 。

### 启动程序

```$ python main.py```


## 使用文档

[**最新文档**](https://wojiaoyishang.gitee.io/tab-toolbox-for-website-document)

## 主页图片

<p align="center">
  <a href="https://layui.github.io/">
    <img src="https://wojiaoyishang.gitee.io/tab-toolbox-for-website-document/_images/quickstart_1.png" width="100%">
  </a>
</p>
