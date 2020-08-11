$(function () {
    $("#danmu-logout").show();
    var loadData = function () {
        $.ajax({
            type: "GET",
            url: "/danmu/super-admin/get/",
            timeout: 5000,
            cache: false,
            success: function (r) {
                var finallist = [];
                var cutlen = Math.ceil(r.length / 4);
                finallist.push(r.slice(0, cutlen));
                finallist.push(r.slice(cutlen, 2 * cutlen));
                finallist.push(r.slice(2 * cutlen, 3 * cutlen));
                finallist.push(r.slice(3 * cutlen));
                var finalhtml = new Array(4).fill("");
                finallist.forEach((r, i) => {
                    r.forEach(e => {
                        finalhtml[i] += `<tr><td title="${e["text"]}">${e["text"]}</td><td>${e["studentid"]}</td><td><a vid="${e["_id"]}" href="javascript:void(0)" onclick="deleteData(this)">删除</a></td></tr>`;
                    })
                })
                finalhtml.forEach((r, i) => {
                    $("#result-container-" + (i + 1)).html(r);
                })
                $("#status-monitor").removeClass("text-warning").removeClass("text-danger").addClass("text-success").text("连接成功")
            },
            error: function (r, t, x) {
                $("#status-monitor").removeClass("text-warning").removeClass("text-success").addClass("text-danger").text("连接失败 " + t)
            }
        })
    }
    var deleteData = function (e) {
        var vid = $(e).attr("vid");
        swal("您确定要删除此弹幕吗?", {
            dangerMode: true,
            buttons: true
        }).then((value) => {
            if (value) {
                $.post("/danmu/super-admin/delete/", { id: vid }, function (r) {
                    if (r.status == 1) {
                        swal("删除结果", "删除成功！", "success");
                    }
                    else {
                        swal("删除结果", "删除失败！", "error");
                    }
                    loadData()
                });
            }
        });
    }
    $("#banuser-ban-btn").click(function () {
        swal("请输入用户学号", {
            content: "input",
            icon: "info",
            dangerMode: true,
            buttons: true
        }).then((value) => {
            if (value && value != "") {
                $.post("/danmu/super-admin/banuser/", { studentid: value }, function (r) {
                    if (r.status == 1) {
                        swal("操作结果", "封禁成功！", "success");
                    }
                    else {
                        swal("操作结果", "封禁失败！", "error");
                    }
                    loadBannedUser();
                });
            }
        });
    });
    $("#banuser-rec-btn").click(function () {
        swal("请输入用户学号", {
            content: "input",
            icon: "info",
            dangerMode: true,
            buttons: true
        }).then((value) => {
            if (value && value != "") {
                $.post("/danmu/super-admin/recoveruser/", { studentid: value }, function (r) {
                    if (r.status == 1) {
                        swal("操作结果", "解禁成功！", "success");
                    }
                    else {
                        swal("操作结果", "解禁失败！", "error");
                    }
                    loadBannedUser();
                });
            }
        });
    });
    var loadBannedUser = function () {
        $.get("/danmu/super-admin/getbanneduser/", function (r) {
            var finalhtml = "";
            r.forEach(e => {
                finalhtml += `<tr><td>${e.studentid}</td><td>${e.operator}</td></tr>`;
            })
            $("#banned-users").html(finalhtml);
        })
    }
    var loadBan = function () {
        loadBannedUser();
        $("#banModal").modal("show");
    }
    $(document).ready(function () {
        loadData()
        window.deleteData = deleteData;
        window.loadBan = loadBan;
        setInterval(loadData, 8000);
    })
})