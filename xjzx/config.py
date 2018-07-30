import redis
import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://name:password@host:port/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis配置
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    # session
    SECRET_KEY = "reuling"
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 14  # session 的有效期，单位是秒
    # 项目在磁盘上的目录：__file__：表示当前文件的名称，自己算出来的，避免因为存放路径不同而不能使用
    # os.path.abspath('')获取文件的绝对路径，如：/home/python/Resource/Flask_xjzx/xjzx/config.py
    # os.path.dirname('')获取文件的目录，如：/home/python/Resource/Flask_xjzx/xjzx/
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 文件保存路径
    UPLOAD_FILE_PATH = os.path.join(BASE_DIR, 'static/avatars/')
    # 加入七牛云的访问域名
    QINIU_URL = 'http://oyvzbpqij.bkt.clouddn.com/'


class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/xjzx'


class ProductConfig(Config):
    pass
