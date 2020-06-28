#coding:utf-8
import redis


class Config(object):
    """配置信息"""
    # DEBUG = True

    SECRET_KEY = 'fhdSDFS2hlJOJL'

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:jykjyk@localhost/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PROT = 6379

    # flask_session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PROT)
    SESSION_USE_SIGNER = True # 对cookie中的session_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400 # session数据的有效期  单位秒


class DevelopmentConfig(Config):
    """开发模式配置信息"""
    DEBUG = True
    pass


class ProductConfig(Config):
    """生产环境配置信息"""
    pass

Config_map = {
    'develop': DevelopmentConfig,
    'product': ProductConfig
}