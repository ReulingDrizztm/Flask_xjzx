function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {

    $(".base_info").submit(function (e) {
        e.preventDefault()

        var signature = $("#signature").val()
        var nick_name = $("#nick_name").val()
        var gender = $(".gender:checked").val()

        if (!nick_name) {
            alert('请输入昵称')
            return
        }
        if (!gender) {
            alert('请选择性别')
        }

        // TODO 修改用户信息接口
        $.post('/user/base',{
            'signature':signature,
            'nick_name':nick_name,
            'gender':gender,
            'csrf_token':$('#csrf_token').val()
        },function (data) {
            if(data.result==2){
                // 成功
                // 左侧和右上角的昵称修改
                // 左侧
                $('.user_center_name',window.parent.document).html(nick_name);
                // 右上角
                $('#nick_name',window.parent.document).html(nick_name);
            }
            else if(data.result==1){
                alert('请填写修改内容')
            }
        })
    })
})