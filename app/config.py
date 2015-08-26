# encoding: utf-8
from flask import url_for

import os

# 在Debug时候，不在forward时停止
DEBUG_TB_INTERCEPT_REDIRECTS = False

# 最大的上传文件大小(4M)
MAX_CONTENT_LENGTH = 4 * 1024 * 1024
UPLOADS_DEFAULT_DEST = os.path.join(os.path.dirname(__file__),
                                    'static/uploads')
BABEL_DEFAULT_LOCALE = 'zh_CN'
BABEL_DEFAULT_TIMEZONE = 'CST'
SQLALCHEMY_ECHO = False
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = '19u0sdjpfkasd;lgj10sdkfj'
SECURITY_PASSWORD_SALT = '123QWEasDzXcqazw'
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
SECURITY_EMAIL_SENDER = os.environ['MAIL_DEFAULT_SENDER']
MAIL_USERNAME = os.environ['SMTP_USERNAME']
MAIL_PASSWORD = os.environ['SMTP_PASSWORD']
MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
SECURITY_POST_CHANGE_VIEW = '/settings'
# 默认不发送邮件, 除非设定了环境变量MAIL_SUPPRESS_SEND为False
MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND') or True

# if os.environ['VISUALS_BEST_DATABASE_URL'] is not None:
try:
    SQLALCHEMY_DATABASE_URI = os.environ['VISUALS_BEST_DATABASE_URL']
except KeyError:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

try:
    DEBUG = (os.environ['DEBUG'] == "True")
except KeyError:
    DEBUG = False

SECRET_KEY = '123QWEasDzXcqazw'
IMAGES_PATH = ['app/static/uploads/gallery', 'app/static/uploads/images',
               'app/static/images', 'app/static/pic',]

security_messages = {
    'UNAUTHORIZED': (u'您没有权限查看本信息', 'error'),
    'CONFIRM_REGISTRATION': (u'感谢您的注册，确认信息已经发送到了邮箱 %(email)s, '
                             u'您需要点击确认邮件中的确认链接才可以登录系统',
                             'success'),
    'EMAIL_CONFIRMED': (u'感谢您的注册，您的邮箱已经确认', 'success'),
    'ALREADY_CONFIRMED': (u'邮箱已经被确认', 'info'),
    'INVALID_CONFIRMATION_TOKEN': (u'错误的确认代码', 'error'),
    'EMAIL_ALREADY_ASSOCIATED': (u'邮箱 %(email)s 已经被注册了', 'error'),
    'PASSWORD_MISMATCH': (u'密码不匹配', 'error'),
    'RETYPE_PASSWORD_MISMATCH': (u'两次输入的密码不匹配', 'error'),
    'INVALID_REDIRECT': (u'禁止重定向到其他的域名', 'error'),
    'PASSWORD_RESET_REQUEST': (u'重置密码的邮件已经发送到邮箱 %(email)s.', 'info'),
    'PASSWORD_RESET_EXPIRED': (u'您没有在 %(within)s 内重置您的密码. ' +
                               u'新的重置密码邮件再次发送到了邮箱 %(email)s',
                               'error'),
    'INVALID_RESET_PASSWORD_TOKEN': (u'错误的重置密码验证信息.', 'error'),
    'CONFIRMATION_REQUIRED': (u'邮箱地址需要确认.', 'error'),
    'CONFIRMATION_REQUEST': (u'确认的帮助邮件已经发到到邮箱%(email)s.', 'info'),
    'CONFIRMATION_EXPIRED': (u'您没有在 %(within)s 内确认账号，新的确认账号的邮件' +
                             u'已经发到到邮箱 %(email)s', 'error'),
    'LOGIN_EXPIRED': (u'您没有在 %(within)s 内登陆系统. 新的登陆帮助信息已经发送到' +
                      u'了邮箱 ''%(email)s', 'error'),
    'LOGIN_EMAIL_SENT': (u'登陆的帮助信息已经发送到邮箱 %(email)s', 'success'),
    'INVALID_LOGIN_TOKEN': (u'错误的系统内部登陆验证信息.', 'error'),
    'DISABLED_ACCOUNT': (u'账号被禁用了', 'error'),
    'EMAIL_NOT_PROVIDED': (u'未输入邮箱地址', 'error'),
    'INVALID_EMAIL_ADDRESS': (u'错误的邮箱地址', 'error'),
    'PASSWORD_NOT_PROVIDED': (u'未输入密码', 'error'),
    'PASSWORD_NOT_SET': (u'未设定用户密码', 'error'),
    'PASSWORD_INVALID_LENGTH': (u'密码最低要求6位以上', 'error'),
    'USER_DOES_NOT_EXIST': (u'用户不存在', 'error'),
    'INVALID_PASSWORD': (u'密码错误', 'error'),
    'PASSWORDLESS_LOGIN_SUCCESSFUL': (u'登录成功', 'success'),
    'PASSWORD_RESET': (u'密码重置成功，自动为您登录到了系统', 'success'),
    'PASSWORD_IS_THE_SAME': (u'新密码必须与旧密码不相同', 'error'),
    'PASSWORD_CHANGE': (u'密码修改成功', 'success'),
    'LOGIN': (u'请登录系统查看本页面', 'info'),
    'REFRESH': (u'请重新登录查看本页面', 'info'),
    'LOGIN_NOT_PROVIDED': (u'请输入用户名', 'error'),

}
