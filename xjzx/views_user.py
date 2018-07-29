from flask import Blueprint, session, make_response, render_template, request, jsonify
from utils.captcha.captcha import captcha
from utils.ytx_sdk import ytx_send
import random

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


# 图形验证码
@user_blueprint.route('/image_code')
def image_code():
    # 调用第三方工具，生成图形验证码数据
    name, text, image = captcha.generate_captcha()
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
