/**
 * @description: 获得URL的GET参数
 * @param name 字符串
 * @return 返回有返回对应项，无返回空
 */
function getUrlParam(name) {
    let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    let r = window.location.search.substring(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}

/**
 * @description: 返回字符串第 n 个出现的位置
 * @param str 被找的字符串
 * @param cha 要找的字符串
 * @param num 第几次出现
 * @return 返回有返回对应项，无返回空
 */
function string_find(str, cha, num) {
    var x = str.indexOf(cha);
    for (var i = 0; i < num; i++) {
        x = str.indexOf(cha, x + 1);
    }
    return x;
}

/**
 * @description: 异步 POST 请求并弹出提示
 * @param url 目标url
 * @param data 数据
 * @param success_callback 成功回调，可为不填
 * @param error_callback 失败回调，可为不填
 * @return 返回有返回对应项，无返回空
 */
function ajax_post_request(url, data, success_callback = function (data) {
    layui.use(['toast'], function () {
        let toast = layui.toast;
        if (data['code'] === 0) {
            toast.success({title: '成功', message: data['msg'], position: 'topCenter'});
        } else {
            toast.error({title: '失败', message: data['msg'] + "（错误代码：" + data['code'].toString() + "）", position: 'topCenter'});
        }
    })
}, error_callback = function (data) {
    layui.use(['toast'], function () {
        let toast = layui.toast;
        toast.error({title: '错误', message: "请求出现了异常，请稍后再试......", position: 'topCenter'});
    })
}) {
    layui.use(['jquery'], function () {
        let $ = layui.jquery
        $.ajax({
            url: url,
            type: "post",
            data: data,
            dataType: "json",
            success: function (data) {
                success_callback(data)
            },
            error: function (data) {
                error_callback(data)
            }
        });
    })
}

/**
 * @description: 异步 GET 请求并弹出提示
 * @param url 目标url
 * @param data 数据
 * @param success_callback 成功回调，可为不填
 * @param error_callback 失败回调，可为不填
 * @return 返回有返回对应项，无返回空
 */
function ajax_get_request(url, data, success_callback = function (data) {
    layui.use(['toast'], function () {
        let toast = layui.toast;
        if (data['code'] === 0) {

            toast.success({title: '成功', message: data['msg'], position: 'topCenter'});

        } else {
            toast.error({title: '失败', message: data['msg'] + "（错误代码：" + data['code'].toString() + "）", position: 'topCenter'});
        }
    })
}, error_callback = function (data) {
    layui.use(['toast'], function () {
        let toast = layui.toast;
        toast.error({title: '错误', message: "请求出现了异常，请稍后再试......", position: 'topCenter'});
    })
}) {
    layui.use(['jquery'], function () {
        let $ = layui.jquery
        $.ajax({
            url: url,
            type: "get",
            data: data,
            dataType: "json",
            success: function (data) {
                success_callback(data)
            },
            error: function (data) {
                error_callback(data)
            }
        });
    })
}