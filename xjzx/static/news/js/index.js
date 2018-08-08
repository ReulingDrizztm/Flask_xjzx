var currentCid = 0; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {
    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid');
        $('.menu li').each(function () {
            $(this).removeClass('active')
        });
        $(this).addClass('active');

        if (clickCid != currentCid) {
            // TODO 去加载新闻数据
            cur_page = 1;
            currentCid = clickCid;
            updateNewsData();

        }
    });

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100 && data_querying==false) {
            // TODO 判断页数，去更新新闻数据
            cur_page += 1;
            if(cur_page <= total_page){
                data_querying = true;
                updateNewsData()
            }

        }
    })
    vue_list_con=new Vue({
        el:'.list_con',
        // 更换{{  }}  为[[  ]]
        delimiters:['[[',']]'],
        data:{
            news_list:[]
        }
    });
    updateNewsData();
});

function updateNewsData() {
    // TODO 更新新闻数据
    $.get('/newslist',{
        'category_id':currentCid,
        'page':cur_page
    },function (data) {
        data_querying=false;
        total_page=data.total_page;
        if(cur_page==1){
            vue_list_con.news_list=data.news_list;
        }else{
            cur_list = vue_list_con.news_list;
            vue_list_con.news_list=cur_list.concat(data.news_list)
        }

    })
}
