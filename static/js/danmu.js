$(function () {
    var lockDown = false;
    var balanceServer = [
        "http://mc.roselle.vip:26170/",
        "http://server3.guidelogin.hcc.io/index.php",
        "http://47.98.170.221/",
        "http://212.64.89.107/",
        "http://katyushaa.asuscomm.com:61080/"
    ];
    var backgroundImage = {
        "large": [
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/large-min-new/background-large-1.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/large-min-new/background-large-2.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/large-min-new/background-large-3.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/large-min-new/background-large-4.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/large-min-new/background-large-5.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/large-min-new/background-large-6.jpg"
        ],
        "small": [
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-1.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-2.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-3.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-4.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-5.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-6.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-7.jpg",
            "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/small-min/background-small-8.jpg"
        ]
    }
    var backgroundInterval;
    var submitButton = $("#send-danmu-form").children("button[type='submit']");
    var iconTranslate = ["https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/boy.png", "https://cdn.jsdelivr.net/gh/yangzhongtian001/imglib@master/girl.png"];
    var fitScreen = function (stagemode = 0) {
        if (stagemode) {
            var send_panel_height = 0;
            var container_height = 0;
            var offset = 0;
        }
        else {
            var send_panel_height = $("#send-panel").height();
            var container_height = $("#navbar-container").height();
            var offset = 42;
        }
        var panelHight = $("body").height() - container_height;
        $(".page-panel").height(panelHight);
        $("#display-panel").height(panelHight - send_panel_height - offset);
    };
    var isMobile = function () {
        var userAgentInfo = navigator.userAgent;
        var mobileAgents = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod"];
        var mobile_flag = false;
        for (var v = 0; v < mobileAgents.length; v++) {
            if (userAgentInfo.indexOf(mobileAgents[v]) > 0) {
                mobile_flag = true;
                break;
            }
        }
        var screen_width = window.screen.width;
        var screen_height = window.screen.height;
        if (screen_width < 500 && screen_height < 800) {
            mobile_flag = true;
        }
        return mobile_flag;
    }
    var fullData = [];
    var fullDatacnt = 0;
    var fullDatalayout = function () {
        var interv = window.setInterval(function () {
            if (fullData.length > 0) {
                if (fullDatacnt >= fullData.length) {
                    clearInterval(interv);
                    fullDatacnt = 0;
                    window.setTimeout(fullDatalayout, 2000);
                }
                $("body").barrager(fullData[fullDatacnt++]);
            }
        }, 500);
    };
    var loadData = function () {
        $.get("/danmu/get/", function (r) {
            fullData = [];
            r.forEach(e => {
                fullData.push({
                    img: iconTranslate[e.icon],
                    href: "#",
                    close: false,
                    info: e.text,
                    color: e.color
                })
            });
        })
    };
    var triggerLoggedin = function () {
        $("#danmu-logout").show();
        loadData();
        window.setInterval(loadData, 10000);
    };
    var loadBalanceServer = function () {
        var callback = location.protocol + "//" + location.host + "/danmu/external_login/?param=";
        var service_name = "在线开学手册";
        var ext_url = "?service_name=" + service_name + "&callback=" + callback;
        balanceServer.forEach((e, i) => {
            $("#balanceServerList").append(`<a class="dropdown-item" href="${e + ext_url}">服务器${i + 1}</a>`)
        })
    };
    var enterStageMode = function (e) {
        $("#navbar-container").hide();
        $("#send-panel").hide();
        $("#display-panel").css("padding", "0px");
        fitScreen(1);
    };
    var danmuBackgroundAutuChange = function () {
        var full = $("#danmu-background li").size();
        var current = 0;
        if (full > 0) $("#danmu-background").find("li").eq(0).show();
        backgroundInterval = window.setInterval(function () {
            if (++current >= full) current = 0;
            $("#danmu-background").find("li").eq(current).fadeIn(500).siblings().fadeOut(500);
        }, 8000)
    }
    var loadDanmuBackground = function (ismobile) {
        var imggroup = ismobile ? backgroundImage["small"] : backgroundImage["large"];
        var finalhtml = "";
        imggroup.forEach(v => {
            finalhtml += `<li style="display:none;"><img src="${v}" class="rounded"></img></li>`;
        })
        $("#danmu-background").html(finalhtml);
    }
    $("#send-danmu-form").submit(function (e) {
        e.preventDefault();
        var danmu_text = $("#danmu-text").val();
        var danmu_color = $("#color-celection").val();
        var danmu_icon = Number($("#icon-celection").val());
        if (danmu_text == "" || lockDown || danmu_text.length > 40) {
            swal("提示", "发送失败：内容为空或长度超过限制", "error");
            return;
        }
        var danmu_config = {
            img: iconTranslate[danmu_icon],
            info: "",
            href: "#",
            close: false,
            color: danmu_color,
            old_ie_color: "#ffffff"
        };
        $("#danmu-text").val("");
        $.post("/danmu/send/", { text: danmu_text, icon: danmu_icon, color: danmu_color }, function (r) {
            if (r.status == 1) {
                danmu_config.info = r.text;
                $("body").barrager(danmu_config);
                lockDown = true;
                submitButton.attr("disabled", true);
                var locktime = 3000;
                setTimeout(function () {
                    lockDown = false;
                    submitButton.attr("disabled", false);
                }, locktime)
            }
            else if (r.status == -2) {
                swal("提示", "您的账号已被封禁", "error");
            }
            else {
                swal("提示", "发送未知错误 状态码" + r.status, "error");
            }
        })
    });
    $("#yunxiao-login").submit(function (e) {
        e.preventDefault();
        var username = $("#yunxiao-username").val();
        var password = $("#yunxiao-password").val();
        var captchacode = $("#yunxiao-captchacode").val();
        var captchavalue = $("#yunxiao-captchavalue").val();
        if (username == "" || password == "") {
            swal("登录失败", "请填写所有内容", "error");
            return;
        }
        $.post("/danmu/login/", { username: username, password: password, captchacode: captchacode, captchavalue: captchavalue }, function (r) {
            if (r.status == 0) {
                $("#loginModal").modal("hide");
                window.location.reload();
            }
            else if (r.status == -1) {
                swal("登录失败", "用户名或密码错误", "error");
            }
            else if (r.status == -2) {
                $("#yunxiao-captchacode").val(r.captchacode);
                $("#yunxiao-captchaarea").show();
                $("#yunxiao-captchadisplay").attr("src", "https://account.yunxiao.com/captcha/" + r.captchacode + "?t=" + new Date().getMilliseconds())
                swal("登录失败", "用户名或密码错误", "error");
            }
            else if (r.status == -3) {
                swal("登录失败", "账号已被冻结请10分钟后再试", "error");
            }
            else if (r.status == 3) {
                swal("登录失败", "验证码已过期请刷新页面", "error");
            }
            else {
                swal("登录失败", "服务器出现了一个未知错误", "error");
            }
        });
    })
    $("#color-celection").colorpicker({
        allowEmpty: false,
        color: "#ffffff",
        showInput: false,
        showInitial: true,
        showPalette: true,
        showSelectionPalette: true,
        showAlpha: false,
        maxPaletteSize: 7,
        preferredFormat: "hex"
    });
    $("#yunxiao-login-local").click(function () {
        $("#yunxiao-login-form").toggle();
        $("#yunxiao-login-submit").toggle();
        $("#yunxiao-login-notice").toggle();
    });
    $("#color-celection").change(function (e) {
        $("#color-celection").css("color", e.value.toString());
    });
    $("#enter-stagemode").click(enterStageMode);
    $(document).ready(function () {
        fitScreen(0);
        $(".selectpicker").selectpicker({
            showIcon: true,
        });
        loadBalanceServer();
        loadDanmuBackground(isMobile());
        fullDatalayout();
        danmuBackgroundAutuChange();
        $(window).resize(function () { fitScreen(0) });
        if (window.loggedIn == "true") {
            triggerLoggedin();
        }
        else {
            $("#loginModal").modal({
                backdrop: "static",
                keyboard: false
            });
        }
    });
})