from datetime import datetime

from flask import Blueprint, request, render_template
from flask import session, redirect, g, current_app
from models import UserInfo

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


# 登录
@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # 判断请求方式,如果是GET方式,返回登录页面,如果是POST,执行登录操作
    if request.method == 'GET':
        return render_template('admin/login.html')

    # 接收
    name = request.form.get('username')
    password = request.form.get('password')

    # 验证
    # 判断非空
    if not all([name, password]):
        return render_template('admin/login.html', msg='请填写用户名和密码')

    # 查询用户信息
    user = UserInfo.query.filter_by(mobile=name, isAdmin=True).first()
    # 判断用户名是否正确
    if user:
        if user.check_pwd(password):
            # 登录成功
            session['admin_id'] = user.id
            # 验证通过,返回后台首页
            return redirect('/admin')
        else:
            return render_template('admin/login.html', msg='您输入的密码不正确')
    else:
        return render_template('admin/login.html', msg='您输入的用户名不存在')


# 创建请求钩子函数,进行登录验证
@admin_blueprint.before_request
def login_avlid():
    ignore_list = ['/admin/login']
    if request.path not in ignore_list:
        if 'admin_id' not in session:
            return redirect('/admin/login')
        g.user = UserInfo.query.get(session.get('admin_id'))


# 退出
@admin_blueprint.route('/logout')
def logout():
    # 删除session
    del session['admin_id']
    return redirect('/admin/login')


# 主页
@admin_blueprint.route('/')
def index():
    return render_template('admin/index.html')


# 用户统计页面
@admin_blueprint.route('/usercount')
def usercount():
    # 用户总数
    total_count = UserInfo.query.filter_by(isAdmin=False).count()

    now = datetime.now()

    # 用户月新增数
    month_first = datetime(now.year, now.month, 1)
    month_count = UserInfo.query.filter_by(isAdmin=False). \
        filter(UserInfo.create_time >= month_first).count()

    # 用户日新增数
    day_first = datetime(now.year, now.month, now.day)
    day_count = UserInfo.query.filter_by(isAdmin=False). \
        filter(UserInfo.create_time >= day_first).count()

    # 用户登录活跃数
    key = 'login' + now.strftime('%Y%m%d')
    redis_cli = current_app.redis_cli
    times = redis_cli.hkeys(key)
    counts = redis_cli.hvals(key)

    times = [item.decode() for item in times]
    counts = [int(item) for item in counts]

    return render_template(
        'admin/user_count.html',
        total_count=total_count,
        month_count=month_count,
        day_count=day_count,
        times=times,
        counts=counts
    )


# 用户列表
@admin_blueprint.route('/user_list')
def user_list():
    pass


# 新闻审核
@admin_blueprint.route('/news_review')
def news_review():
    pass


# 新闻版式编辑
@admin_blueprint.route('/news_edit_detail', methods=['GET', 'POST'])
def news_edit_detail():
    pass


# 新闻分类管理--查询
@admin_blueprint.route('/news_type')
def news_type():
    pass
