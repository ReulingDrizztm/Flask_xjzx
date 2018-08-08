from datetime import datetime
from flask import current_app
from flask_script.commands import Command
from models import UserInfo, db
import random


class CreateAdmin(Command):
    def run(self):
        # 接收数据
        nick_name = input("请输入用户名:")
        password = input("请输入密码:")

        # 创建管理员账户对象,并赋值
        user = UserInfo()
        user.mobile = nick_name
        user.nick_name = nick_name
        user.password = password
        user.isAdmin = True

        # 提交到数据库
        db.session.add(user)
        db.session.commit()

        # 显示创建结果
        print("管理员%s创建成功!" % nick_name)


class LoginTest(Command):
    def run(self):
        now = datetime.now()

        redis_cli = current_app.redis_cli
        key = 'login' + now.strftime('%Y%m%d')

        for index in range(8, 20):
            redis_cli.hset(key, '%02d:00' % index, random.randint(180, 300))

        print("OK")
