import re

from flask import Blueprint, session, make_response, render_template, request, jsonify
from flask import g
from flask import redirect

from models import UserInfo, db
from utils.captcha.captcha import captcha
from utils.ytx_sdk import ytx_send

import random

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


# 图形验证码
@user_blueprint.route('/image_code')
def image_code():
    # 调用第三方工具，生成图形验证码数据
    name, text, image = captcha.generate_captcha()
    print(text)
    # 保存数据，用于后续验证
    session['image_code'] = text
    # 创建响应对象，相应体为图片数据
    response = make_response(image)
    # 设置相应体的类型为图片
    response.content_type = 'image/png'
    # 返回响应体
    return response


# 手机验证码
@user_blueprint.route('/sms_code')
def sms_code():
    # 接收
    mobile = request.args.get('mobile')
    imagecode = request.args.get('imagecode')
    # 验证
    if not all([mobile, imagecode]):
        return jsonify(result=1)

    imagecode_session = session.get('image_code')
    if not imagecode_session:
        return jsonify(result=2)

    # 强制图形验证码过期
    del session['image_code']
    if imagecode_session != imagecode:
        return jsonify(result=3)

    # 处理
    # 生成随机验证码：
    smscode = str(random.randint(100000, 999999))
    # 保存验证码，用于后续验证
    session['sms_code'] = smscode
    # 发送验证码到用户注册的手机号码上
    # ytx_send.sendTemplateSMS(mobile, [smscode, '10'], 1)
    print(smscode)

    # 响应
    return jsonify(result=4)


# 注册
@user_blueprint.route('/signup', methods=['POST'])
def signup():
    # 接收
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    smscode = request.form.get('smscode')

    # 验证
    # 验证信息是否填写完整
    if not all([mobile, password, smscode]):
        return jsonify(result=1)
    # 验证手机验证码是否正确
    # 获取手机验证码
    smscode_session = session.get('sms_code')
    # 获取完手机验证码之后立即删除session中的信息
    del session['sms_code']
    if not smscode_session:
        return jsonify(result=2)
    # 判断用户输入的手机验证码和服务端保存的是否一致
    if smscode != smscode_session:
        return jsonify(result=3)
    # 判断用户是否已经注册过了
    # if UserInfo.query.filter_by(mobile=mobile).count() > 0:
    if UserInfo.query.filter_by(mobile=mobile).count() > 0:
        return jsonify(result=4)
    # 验证密码是否合法
    if not re.match(r'^[0-9a-zA-Z]{6,20}$', password):
        return jsonify(result=5)

    # 处理
    user = UserInfo()
    user.mobile = mobile
    user.password = password
    user.nick_name = mobile

    # 保存到数据库里面
    db.session.add(user)
    db.session.commit()

    # 响应
    return jsonify(result=6)


# 登录
@user_blueprint.route('/signin', methods=['POST'])
def signin():
    # 接收
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    # 验证
    if not all([mobile, password]):
        return jsonify(result=1)

    # 处理:根据手机号查询用户信息，然后进行对比
    user = UserInfo.query.filter_by(mobile=mobile).first()
    if not user:
        # 如果没有查到数据，则返回NONE
        # 表示手机号码错误
        return jsonify(result=2)
    # 验证密码是否正确
    if user.check_pwd(password):
        # 状态保持
        session['user_id'] = user.id
        # 密码正确
        return jsonify(result=4, nick_name=user.nick_name, avatar=user.avatar)
    else:
        # 密码错误
        return jsonify(result=3)


# 退出
@user_blueprint.route('/signout')
def signout():
    # 退出
    if 'user_id' in session:
        del session['user_id']
    return jsonify(result=1)


# 用户中心
@user_blueprint.route('/')
def index():
    # 判断用户是否登陆，如果没有登陆直接输入了地址，则重定向到首页去登录
    if 'user_id' not in session:
        return redirect('/')
    # 查询当前登录的用户
    user_id = session.get('user_id')
    g.user = UserInfo.query.get(user_id)
    print(user_id)
    return render_template(
        'news/user.html',
        title='用户中心',
    )


# 基本资料
@user_blueprint.route('/base', methods=['GET', 'POST'])
def base():
    # 查询当前用户是否登录，如果没有登录，跳转到首页登录
    if 'user_id' not in session:
        return redirect('/')
    # 获取当前用户的基本信息
    g.user = UserInfo.query.get(session.get('user_id'))
    # 如果是发起的GET请求，返回用户基本信息页面
    if request.method == 'GET':
        return render_template('news/user_base_info.html')

    # 如果是POST请求，就修改用户基本信息
    # 接收
    signature = request.form.get('signature')
    nick_name = request.form.get('nick_name')
    gender = request.form.get('gender')

    # 验证
    if not all([signature, nick_name, gender]):
        return jsonify(result=1)

    # 处理
    # 拿到当前对象
    user = g.user
    # 给当前对象赋值
    user.signature = signature
    user.nick_name = nick_name
    # 所有从报文中拿到的数据都是字符串，都会返回1，只有空字符串会转换成0
    user.gender = bool(int(gender))
    # 提交，保存修改
    db.session.commit()

    # 响应
    return jsonify(result=2)
