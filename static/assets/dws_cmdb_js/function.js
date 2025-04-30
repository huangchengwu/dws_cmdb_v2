

$(document).ready(function () {

    $('.show_password').click(function () {

        // 检查Cookie是否存在且未过期
        var existingCookie = document.cookie.replace(/(?:(?:^|.*;\s*)password\s*\=\s*([^;]*).*$)|^.*$/, "$1");
        var cookieExpiration = document.cookie.replace(/(?:(?:^|.*;\s*)password_expires\s*\=\s*([^;]*).*$)|^.*$/, "$1");

        var now = new Date().getTime();
        var expiration = new Date(cookieExpiration).getTime();

        href = $(this).attr('href');





        if (existingCookie && expiration > now) {
            id = $(this).attr('value');




            $.ajax({
                type: "POST",

                url: '/ConfCen/HostConfig/' + id + '/show_password/',
                headers: {
                    'X-CSRFToken': csrfToken
                },

                cache: false,
                dataType: "json",
                data: {
                    "password": existingCookie
                },
                success: function (msg) {
                   
                    if (href == "#true") {

                        window.location.href = "/admin/ConfCen/hostconfig/" + id + "/change/"
                    }else{
                        alert(msg.msg);
                    }

                }
            });

        } else {
            var password = prompt("请输入密码");

            id = $(this).attr('value');


            $.ajax({
                type: "POST",

                url: '/ConfCen/HostConfig/' + id + '/show_password/',
                headers: {
                    'X-CSRFToken': csrfToken
                },

                cache: false,
                dataType: "json",
                data: {
                    "password": password
                },
                success: function (msg) {

                    // 简单示例验证，密码为"password"时登录成功
                    if (msg.status === true) {
                        // 验证通过，存储用户名到Cookie中，有效期1小时
                        var expirationTime = new Date(now + 1 * 60 * 60 * 1000).toUTCString();
                        document.cookie = "password=" + password + "; expires=" + expirationTime;
                        document.cookie = "password_expires=" + expirationTime + "; expires=" + expirationTime;
                        if (href == "#true") {

                            window.location.href = "/admin/ConfCen/hostconfig/" + id + "/change/"
                        }else{
                            alert(msg.msg);
                        }
                       
                    } else {
                        alert("登录失败，请输入正确的密码！");
                    }

                }
            });
       

        }
    });


});
