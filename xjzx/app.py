from flask import Flask
from flask import render_template
from models import db
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import logging
from logging.handlers import RotatingFileHandler
from views_news import news_blueprint
from views_admin import admin_blueprint
from views_user import user_blueprint


def create_app(Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    redis_cli = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
    app.redis_cli = redis_cli

    CSRFProtect(app)

    Session(app)

    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(Config.BASE_DIR + "/logs/xjzx.log", maxBytes=1024 * 1024 * 100,
                                           backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
    app.logger_xjzx = logging

    # 注册蓝图
    # 注册new蓝图
    app.register_blueprint(news_blueprint)
    # 注册register蓝图
    app.register_blueprint(admin_blueprint)
    # 注册user蓝图
    app.register_blueprint(user_blueprint)

    @app.errorhandler(404)
    def handle404(e):
        return render_template('news/404.html')

    return app
