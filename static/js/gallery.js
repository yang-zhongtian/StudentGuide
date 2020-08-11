$(function () {
    var config = {
        "直升初一": "",
        "常规初一": "",
        "直升初二": "",
        "常规初二": "",
        "初三": "",
        "直升高一": "",
        "高一": "",
        "高二": "",
        "高三": "",
        "国际部高一": "",
        "国际部高二": "",
        "国际部高三": ""
    }
    var loadData = function () {
        $(".v-bind").each(function () {
            var url = config[$(this).text()];
            if (url == "") url = 'javascript: swal("错误","该年级数据未导入！","error")';
            $(this).attr("href", url);
        })
    }
    loadData();
});