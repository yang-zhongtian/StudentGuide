$(function () {
    $("#danmu-logout").show();
    var currentDataLength = -1;
    var currentSelected = -1;
    var lazyLoadTimer;
    var firstPressTime = 0;
    var keyCaptureOn = true;
    toastr.options = {
        progressBar: true,
        timeOut: 2000
    }
    var loadData = function (firstrun = 0) {
        $.ajax({
            type: "GET",
            url: "/danmu/super-admin/get/?verifier=" + $("#verifier-select").val(),
            timeout: 5000,
            cache: false,
            success: function (r) {
                var finallist = r;
                var finalhtml = "";
                currentDataLength = finallist.length;
                currentSelected = 0;
                finallist.forEach(e => {
                    finalhtml += `<tr class="row mx-0" v-data="${e["_id"]}"><td v-bind="cursor" class="col-1"></td><td title="${e["text"]}" class="col-5">${e["text"]}</td><td class="col-4">${e["username"]}</td><td class="col-2"></td></tr>`;
                })
                $("#result-container").html(finalhtml);
                $("#status-monitor").removeClass("text-warning").removeClass("text-danger").addClass("text-success").text("连接成功")
                if (currentDataLength > 0) {
                    clearInterval(lazyLoadTimer)
                    lazyLoadTimer = undefined;
                    if(!firstrun) $("#alert-audio").attr("src", $("#alert-audio").attr("src"));
                    $("#result-container").find("tr").eq(0).find("td").eq(0).text(">");
                    tagAsActive(0);
                }
                else {
                    if (lazyLoadTimer == undefined) lazyLoadTimer = setInterval(loadData, 5000);
                }
            },
            error: function (r, t, x) {
                $("#status-monitor").removeClass("text-warning").removeClass("text-success").addClass("text-danger").text("连接失败 " + t)
            }
        })
    }
    var tagAsActive = function (nth) {
        $("#result-container").find("tr").eq(nth).addClass("table-info").siblings().removeClass("table-info");
    }
    var tagAsDelete = function (nth) {
        var element = $("#result-container").find("tr").eq(nth).find("td").eq(3);
        if (element.html() == "") {
            element.html('<i class="fas fa-check"></i>')
        }
        else {
            element.html('')
        }
    }
    var packToServer = function () {
        if (currentDataLength <= 0) return;
        accept_id = [];
        delete_id = [];
        $("#result-container").find("tr").each(function () {
            var node = $(this);
            var is_delete = node.find("td").eq(3).html() == "" ? false : true;
            if (is_delete) delete_id.push(node.attr("v-data"));
            else accept_id.push(node.attr("v-data"));
        })
        $.post("/danmu/super-admin/operation/", { "accept_id": accept_id, "delete_id": delete_id }, function (r) {
            toastr.success("审核数据提交成功！", "提示")
            loadData();
        })
    }
    $("#banuser-ban-btn").click(function () {
        swal("请输入用户学号", {
            content: "input",
            icon: "info",
            dangerMode: true,
            buttons: true
        }).then((value) => {
            if (value && value != "") {
                $.post("/danmu/super-admin/banuser/", { username: value }, function (r) {
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
                $.post("/danmu/super-admin/recoveruser/", { username: value }, function (r) {
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
    $("#verifier-select").change(function () {
        loadData()
    })
    $(document).keydown(function (event) {
        if (keyCaptureOn === false) return true;
        switch (event.keyCode) {
            case 83: // S
                if (currentSelected < currentDataLength - 1) {
                    $("#result-container").find("tr").eq(currentSelected++).find("td").eq(0).text("");
                    $("#result-container").find("tr").eq(currentSelected).find("td").eq(0).text(">");
                    tagAsActive(currentSelected);
                }
                return false;
            case 87: // W
                if (currentSelected > 0) {
                    $("#result-container").find("tr").eq(currentSelected--).find("td").eq(0).text("");
                    $("#result-container").find("tr").eq(currentSelected).find("td").eq(0).text(">");
                    tagAsActive(currentSelected);
                }
                return false;
            case 65: // A
                tagAsDelete(currentSelected);
                return false;
            case 68: // D
                var firstTime = new Date().getTime();
                if (firstPressTime == 0) {
                    firstPressTime = firstTime;
                } else {
                    var lastTime = new Date().getTime();
                    console.log("CURRENT timestamp", lastTime);
                    console.log("Time elapse", lastTime - firstPressTime);
                    if (lastTime - firstPressTime < 800) {
                        packToServer();
                        firstPressTime = 0;
                    }
                    else {
                        firstPressTime = lastTime;
                    }
                }
                return false;
        };
        return true;
    });
    $("#result-container").click(function (e) {
        var element = $(e.target).parent("tr");
        var indexes = $("#result-container tr").index(element);
        if (currentSelected == indexes) tagAsDelete(indexes);
        else {
            currentSelected = indexes;
            $("#result-container").find("tr").each(function () {
                $(this).find("td").eq(0).text("")
            });
            $("#result-container").find("tr").eq(currentSelected).find("td").eq(0).text(">");
            tagAsActive(currentSelected);
        }
    })
    var loadBannedUser = function () {
        $.get("/danmu/super-admin/getbanneduser/", function (r) {
            var finalhtml = "";
            r.forEach(e => {
                finalhtml += `<tr><td>${e.username}</td><td>${e.operator}</td></tr>`;
            })
            $("#banned-users").html(finalhtml);
        })
    }
    var loadBan = function () {
        loadBannedUser();
        $("#banModal").modal("show");
        keyCaptureOn = false;
    }
    var loadVerifier = function () {
        var verify = $("#verifier-select");
        var html_text = "";
        for (var i = 1; i <= Number(verify.attr("count")); i++) {
            html_text += `<option value="${i}">${i}</option>`;
        }
        verify.html(html_text);
    }
    var manualSubmit = function () {
        swal("确认", {
            text: "是否确认提交审核数据？",
            icon: "warning",
            buttons: true
        }).then((value) => {
            if (value && value != "") {
                packToServer();
            }
        });
    }
    var dismissBanDialog = function () { keyCaptureOn = true };
    $(document).ready(function () {
        window.loadBan = loadBan;
        window.manualSubmit = manualSubmit;
        window.dismissBanDialog = dismissBanDialog;
        loadVerifier()
        loadData(1)
    })
})