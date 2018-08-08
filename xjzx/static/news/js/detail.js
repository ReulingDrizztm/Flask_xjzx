function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    vue_comment_list_con = new Vue({
        el: '.comment_list_con',
        delimiters: ['[[', ']]'],
        data: {
            comment_list: []
        }
    });

    loadcommentlist();

    // 收藏
    $(".collection").click(function () {
        $.post('/collect', {
            'news_id': $('#news_id').val(),
            'csrf_token': $('#csrf_token').val()
        }, function (data) {
            if (data.result == 1) {
                //未登录，则弹出登录窗口
                $('.login_form_con').show();
            } else if (data.result == 4) {
                //收藏成功
                $('.collection').hide();
                $('.collected').show();
            }
        });
    })

    // 取消收藏
    $(".collected").click(function () {
        $.post('/collect', {
            'news_id': $('#news_id').val(),
            'csrf_token': $('#csrf_token').val()
        }, function (data) {
            if (data.result == 4) {
                //取消收藏成功
                $('.collection').show();
                $('.collected').hide();
            }
        });
    })

    // 评论提交
    $(".comment_form").submit(function (e) {
        e.preventDefault();
        var news_id = $('#news_id').val();
        var msg = $('.comment_input').val();
        if (msg.length <= 0) {
            alert('请填写评论内容');
        }
        $.post('/comment_add', {
            'news_id': news_id,
            'msg': msg,
            'csrf_token': $('#csrf_token').val()
        }, function (data) {
            if (data.result == 3) {
                //评论成功
                $('.comment_input').val('');
                //刷新列表
                loadcommentlist();
            }
        });
    })

    $('.comment_list_con').delegate('a,input', 'click', function () {

        var sHandler = $(this).prop('class');

        if (sHandler.indexOf('comment_reply') >= 0) {
            $(this).next().toggle();
        }

        if (sHandler.indexOf('reply_cancel') >= 0) {
            $(this).parent().toggle();
        }

        if (sHandler.indexOf('comment_up') >= 0) {
            var $this = $(this);
            if (sHandler.indexOf('has_comment_up') >= 0) {
                // 如果当前该评论已经是点赞状态，再次点击会进行到此代码块内，代表要取消点赞
                $this.removeClass('has_comment_up')
            } else {
                $this.addClass('has_comment_up')
            }
        }

        if (sHandler.indexOf('reply_sub') >= 0) {
            var back_content=$(this).prev();
            var form=$(this).parent();
            var news_id=$('#news_id').val();
            var msg=$(this).prev().val();
            var comment_id=$(this).attr('name');
            $.post('/comment_add', {
                'news_id': news_id,
                'msg': msg,
                'comment_id':comment_id,
                'csrf_token': $('#csrf_token').val()
            }, function (data) {
                if (data.result == 3) {
                    //评论成功
                    back_content.val('');
                    form.hide();
                    //刷新列表
                    loadcommentlist();
                }
            });
        }
    })

    // 关注当前新闻作者
    $(".focus").click(function () {
        $.post('/follow',{
            'author_id':$('#author_id').val(),
            'csrf_token':$('#csrf_token').val()
        },function (data) {
            if(data.result==3){
                $('.focus').hide();
                $('.focused').show();
            }
        });
    })

    // 取消关注当前新闻作者
    $(".focused").click(function (e) {
        e.preventDefault();
        $.post('/follow',{
            'author_id':$('#author_id').val(),
            'csrf_token':$('#csrf_token').val()
        },function (data) {
            if(data.result==3){
                $('.focus').show();
                $('.focused').hide();
            }
        });
    })
})

function loadcommentlist() {
    var news_id = $('#news_id').val();
    $.get('/comment_list/' + news_id, function (data) {
        vue_comment_list_con.comment_list = data.list;
    });
}