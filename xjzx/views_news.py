# from flask import Blueprint, render_template, session, g, jsonify, abort
# from flask import request
# from models import NewsCategory, UserInfo, NewsInfo, db, NewsComment

from flask import Blueprint, render_template, session, g, request, jsonify, abort
from models import NewsCategory, UserInfo, NewsInfo, db, NewsComment

news_blueprint = Blueprint('news', __name__)


# 主页
@news_blueprint.route('/')
def index():
    # 接收：没有参数传入，不需要接收
    # 验证：没有接收任何参数，不需要验证
    # 处理
    # 分类
    category_list = NewsCategory.query.all()
    # 登录状态
    if 'user_id' in session:
        g.user = UserInfo.query.get(session.get('user_id'))
    else:
        g.user = None
    # 点击排行
    click_list = NewsInfo.query.order_by(NewsInfo.click_count.desc())[0:6]
    # 响应
    return render_template(
        'news/index.html',
        category_list=category_list,
        click_list=click_list,
        title='首页'
    )


# 显示新闻列表
@news_blueprint.route('/newslist')
def newslist():
    # 接收
    page = int(request.args.get('page', 1))
    category_id = int(request.args.get('category_id', 0))

    # 验证:如果没有page则为默认值1,如果没有category_id则为默认值0

    # 处理
    # 查询的时候进行sql语句的拼接,直到使用数据的时候,才会执行查询的代码,如for遍历数据
    query = NewsInfo.query
    # select * from NewsInfo
    if category_id > 0:
        # 如果编号等于0,表示查询所有新闻,所有分类
        # 如果编号大于0,表示查询某个对应的分类
        query = query.filter_by(category_id=category_id)
        # 相当于where语句
    # 排序,分页
    query = query.order_by(NewsInfo.id.desc()).paginate(page, 4, False)
    # 获取当前页的数据
    news_list = query.items
    # 总页数
    total_page = query.pages

    # news对象无法直接转成json语句,需要先转成字典,再转成json数据
    # 获取数据,转成字典
    news_list2 = []

    # 在这里才是在mysql中执行查询,获取数据
    for news in news_list:
        news_list2.append({
            'id': news.id,
            'pic': news.pic_url,
            'title': news.title,
            'summary': news.summary,
            'avatar': news.user.avatar_url,
            'nick_name': news.user.nick_name,
            # python中的DateTime类型有个方法strrftime()日期格式化,转成字符串
            'create_time': news.create_time.strftime('%Y-%m-%d %H:%M:%S'),

        })

    # 响应
    return jsonify(news_list=news_list2, total_page=total_page)


# 新闻详情页
@news_blueprint.route('/<int:news_id>')
def detail(news_id):
    # 判断用户的登录状态
    if 'user_id' in session:
        # 如果已经登录,就把用户的信息查询出来
        g.user = UserInfo.query.get(session.get('user_id'))
    else:
        # 如果没有登录,用户的信息就为空值
        g.user = None

    # 根据主键查询新闻的信息
    news = NewsInfo.query.get(news_id)
    # 判断是否查询到新闻对象,如果没有查到,就返回404页面
    if not news:
        abort(404)

    # 查询到了新闻对象,点击量加一
    news.click_count += 1
    db.session.commit()

    # 查询出点击排行榜
    click_list = NewsInfo.query.order_by(NewsInfo.click_count.desc())[0:6]
    # 将数据显示到模板中
    return render_template(
        'news/detail.html',
        click_list=click_list,
        news=news,
        title="文章详情页"
    )


# 收藏与取消收藏
@news_blueprint.route('/collect', methods=['POST'])
def collect():
    # 接收
    news_id = request.form.get('news_id')

    # 判断用户是否登录
    if 'user_id' not in session:
        return jsonify(result=1)
        # return redirect('/user/signin')

    # 判断是否为空
    if not news_id:
        return jsonify(result=2)

    # 判断news_id是否合法
    # 通过新闻的编号获取新闻信息
    news = NewsInfo.query.get(news_id)
    if not news:
        return jsonify(result=3)
    # 处理
    # 获取用户信息
    user = UserInfo.query.get(session.get('user_id'))
    # 多对多数据结构,通过关系属性向关系表中添加数据
    if news not in user.news_collect:
        user.news_collect.append(news)
    else:
        # 如果数据库中已经有相关信息,表示已经关注过了,再次点"关注"就是取消关注
        user.news_collect.remove(news)
    # 提交到数据库中去
    db.session.commit()

    # 响应"
    return jsonify(result=4)


# 评论与回复
@news_blueprint.route('/comment_add', methods=['POST'])
def comment_add():
    # 判断用户是否登录
    if 'user_id' not in session:
        return jsonify(result=1)

    # 接收
    msg = request.form.get('msg')
    news_id = request.form.get('news_id')
    comment_id = int(request.form.get('comment_id', 0))

    # 验证
    if not all([msg, news_id]):
        return jsonify(result=2)

    # 处理
    comment = NewsComment()
    comment.msg = msg
    comment.news_id = int(news_id)
    comment.user_id = session.get('user_id')

    # 判断评论id是否为0
    if comment_id > 0:
        comment.comment_id = comment_id

    comment.comment_count += 1
    db.session.add(comment)
    db.session.commit()

    # 响应
    return jsonify(result=3)


# 评论列表与回复列表
@news_blueprint.route('/comment_list/<int:news_id>')
def comment_list(news_id):
    # 处理：查询指定新闻的评论信息
    list1 = NewsComment.query. \
        filter_by(news_id=news_id, comment_id=None). \
        order_by(NewsComment.id.desc())

    # 将对象转字典
    list2 = []
    for comment in list1:
        # 根据评论对象comment获取所有的回复对象
        back_list = []
        for back in comment.backs:
            back_list.append({
                'id': back.id,
                'msg': back.msg,
                'nick_name': back.user.nick_name,
            })

        list2.append({
            'id': comment.id,
            'msg': comment.msg,
            'avatar': comment.user.avatar_url,
            'nick_name': comment.user.nick_name,
            'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'like_count': comment.like_count,
            'back_list': back_list
        })

    # 响应
    return jsonify(list=list2)


# 关注与取消关注
@news_blueprint.route('/follow', methods=['POST'])
def follow():
    # 接收
    author_id = request.form.get('author_id')

    # 验证
    # 1.作者编号非空
    if not author_id:
        return jsonify(result=1)
    # 2.用户登录
    if 'user_id' not in session:
        return jsonify(result=2)
    user_id = session.get('user_id')
    # 查询对象
    user = UserInfo.query.get(user_id)
    author = UserInfo.query.get(author_id)

    # 处理：判断是否关注
    if author in user.authors:
        # 取消
        user.authors.remove(author)
        # 粉丝数-1
        author.follow_count -= 1
        print(author.follow_count)
    else:
        # 关注
        user.authors.append(author)
        # 粉丝数+1
        author.follow_count += 1
        print(author.follow_count)
    # 提交到数据库
    db.session.commit()

    # 响应
    return jsonify(result=3)
