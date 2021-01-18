from flask import Flask
from flask_login import LoginManager
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# ###############应用程序######################
app = Flask(__name__)


# #################配置########################
app.config.from_object(Config)  # app.config['SECRET_KEY'] = 'you-will-never-guess' # 添加配置


# #################数据库#####################
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# #################登录########################
login = LoginManager(app)
login.login_view = 'login'  # 哪个视图函数用于处理登录认证,上面的'login'值是登录视图函数（endpoint）名，换句话说该名称可用于url_for()函数的参数并返回对应的URL

# # ##############记录错误信息到邮件################----没有实现，需要再试试
# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         print(app.config['MAIL_SERVER'])
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#             toaddrs=app.config['ADMINS'],
#             subject='Microblog Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         app.logger.addHandler(mail_handler)

# # ##############记录错误信息到日志文件################
if not app.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


# ############从包app中导入routes，这里的app不是上述的app变量###########
from app import routes, models, errors
