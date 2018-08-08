function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    $(".pass_info").submit(function (e) {
        e.preventDefault()

        var initial_password = $("#initial_password").val()
        var new_password = $("#new_password").val()
        var confirm_password = $("#confirm_password").val()

        if (!initial_password) {
            alert('请输入当前密码')
            return
        }
        if (!new_password) {
            alert('请输入新密码')
            return
        }
        if (!confirm_password) {
            alert('请再次输入密码')
            return
        }

        $.post('/user/password', {
            'initial_password': initial_password,
            'new_password': new_password,
            'confirm_password': confirm_password,
            'csrf_token': $('#csrf_token').val()
        }, function (data) {
            if (data.result == 1) {
                alert('请填写当前使用的密码')
            }
            else if (data.result == 2) {
                alert('当前密码不正确')
            }
            else if (data.result == 3) {
                alert('新密码请不要和当前密码相同')
            }
            else if (data.result == 4) {
                alert('两次输入的密码不一样')
            }
            else if (data.result == 5) {
                alert('修改成功，请妥善保管您的密码')
            }
        })
    })
})