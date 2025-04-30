
var csrfToken = "{{ csrf_token }}";
$('#tasklist').DataTable({
    "order": [[0, "desc"]]
})

$(document).ready(function () {
    $('button[name="task_disable"]').click(function () {
        var buttonValue = $(this).val();

        alert('中止任务: ' + buttonValue);

        $.ajax({
            type: "DELETE",
            url: '/DeployCen/TaskDeploy/' + buttonValue + '/task_disable/',
            headers: {
                'X-CSRFToken': csrfToken // 使用JavaScript变量添加CSRF令牌
            },

            cache: false,
            dataType: "json",
            data: {

            },
            success: function (msg) {
                alert('中止任务: ' + buttonValue);

                location.reload(); // 异步刷新

            }
        });
        location.reload();
    });

    setInterval(function () {
        location.reload(); // 异步刷新
    }, 15000); // 设置间隔时间为 60000 毫秒（即 60 秒）
    function task_disable() {
        alert("中止任务");
    }
    $('#task_disable').click(function () {

        alert("中止任务");
        // id = $(this).attr('value');
        // $.ajax({
        //     type: "DELETE",
        //     url: '/DeployCen/TaskDeploy/' + id + '/task_disable/',
        //     headers: {
        //         'X-CSRFToken': csrfToken // 使用JavaScript变量添加CSRF令牌
        //     },

        //     cache: false,
        //     dataType: "json",
        //     data: {

        //     },
        //     success: function (msg) {
        //         alert("任务中止");
        //         location.reload(); // 异步刷新

        //     }
        // });

    });






    $('#deploy_app').click(function () {
        // 在这里添加按钮点击后执行的操作
        var value = $(this).val();
        alert("fabu")
        $.ajax({
            type: "post",
            url: '/deploy_app/',
            cache: false,
            dataType: "json",
            data: {
                "deploy_app": $("#deploy_app").val(),
            },
            success: function (msg) {
                alert(msg);
            }
        });

        alert(value);
        location.reload();
    });

    $('#uninstall').click(function () {
        // 在这里添加按钮点击后执行的操作
        alert('uninstall');
        location.reload();
    });

});