$(function () {
    var config = {
        "直升初一": "",
        "常规初一(张潇文)": "https://www.bilibili.com/blackboard/player.html?aid=329422249&bvid=BV1CA411n7tb&cid=229439539",
        "常规初一(陈纹珊)": "https://www.bilibili.com/blackboard/player.html?aid=926907683&bvid=BV1BT4y1L7nn&cid=229438759",
        "直升初二": "https://www.bilibili.com/blackboard/player.html?aid=244474076&bvid=BV1Hv411177f&cid=229623025",
        "常规初二": "https://www.bilibili.com/blackboard/player.html?aid=884413805&bvid=BV1pK4y1e7vw&cid=229321093",
        "初三": "https://www.bilibili.com/blackboard/player.html?aid=839454822&bvid=BV1654y1276i&cid=229323852",
        "直升高一": "",
        "高一": "https://www.bilibili.com/blackboard/player.html?aid=669413833&bvid=BV1da4y1773P&cid=229324509",
        "高二": "https://www.bilibili.com/blackboard/player.html?aid=669411382&bvid=BV19a4y177n8&cid=229325495",
        "高三": "https://www.bilibili.com/blackboard/player.html?aid=626952278&bvid=BV1et4y1S7Yx&cid=229326416",
        "国际部高一": "",
        "国际部高二": "https://rrx.cn/view-wwq3yq",
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