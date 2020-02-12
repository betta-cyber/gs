$("#generate").click(function () {
    var os = $("#os").val();
    var ip = $("#ip").val();
    var port = $("#port").val();
    var username = $("#username").val();
    var password = $("#password").val();

    $.ajax({
        type: "POST",
        url: "/task",
        contentType: "application/json",
        data: JSON.stringify({
            "os": os,
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
        }),
        dataType: "json",
        success: function (message) {
            alert("任务添加成功");
        },
        error: function (message) {
            alert("提交失败" + JSON.stringify(message));
        }
    });
})