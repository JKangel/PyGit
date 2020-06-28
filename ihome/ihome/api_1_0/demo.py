#coding:utf-8

from . import api
from ihome import db, models
import logging
from flask import current_app


@api.route('/index')
def index():
    # logging.error("") # 错误级别
    # logging.warn("") # 警告级别
    # logging.info("") # 信息级别
    # logging.debug("") # 调试级别
    current_app.logger.error('error message')
    current_app.logger.warn('warn message')
    current_app.logger.info('info message')
    current_app.logger.debug('debug message')
    return 'index page'