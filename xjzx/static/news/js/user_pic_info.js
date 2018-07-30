function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    $(".pic_info").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/portrait',
            type:'post',
            dataType:'json',
            // 'csrf_token':$('#csrf_token').val(),
            success:function (data) {
                // 更新当前页面的头像
                $('.now_user_pic').attr('src',data.avatar);
                // 更新左侧的头像
                $('.user_center_pic img', window.parent.document).attr('src',data.avatar);
                // 更新右上角的头像
                $('.lgin_pic', window.parent.document).attr('src',data.avatar);
            }
        });
    });
})