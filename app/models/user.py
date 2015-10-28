# coding=utf-8
from app import const

from app.app_provider import AppInfo
from app.const import USER_STATUS_UN_VERIFIED, USER_STATUS_VERIFIED
from app.models.enum_values import EnumValues
from flask.ext.security import RoleMixin, UserMixin
from image import Image
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Date, Numeric, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()

roles_users = db.Table('roles_users', db.Column('id', db.Integer(), primary_key=True),
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

users_styles = db.Table('users_styles', db.Column('id', db.Integer(), primary_key=True),
                        db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), nullable=False),
                        db.Column('style_id', db.Integer(), db.ForeignKey('enum_values.id'), nullable=False))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return self.name


class User(db.Model, UserMixin):
    # To name the table users is to avoid conflict with postgresSQL OOTB user
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    login = db.Column(db.String(64), unique=True, nullable=False)
    display = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    mobile_phone = db.Column(db.String(16), nullable=False)
    qq_number = db.Column(db.String(16), nullable=True)
    wechat_account = db.Column(db.String(32), nullable=True)
    weibo_account = db.Column(db.String(32), nullable=True)
    introduce = db.Column(Text, nullable=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    styles = db.relationship(EnumValues, secondary=users_styles,
                             backref=db.backref('users_of_style', lazy='dynamic'))
    gender = db.Column(db.String(8), nullable=True)
    birthday = db.Column(Date, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)

    # 该用户是由哪个用户推荐的
    recommend_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recommend_by = db.relation("User", remote_side=id, backref=backref(
        'recommended_users', uselist=True))

    # 头像
    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    image = db.relation(Image, backref='image_user')

    # 用户类型
    type_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    type = relationship('EnumValues', backref=backref(
        'users_of_type', uselist=True), foreign_keys=[type_id])

    # 每天的报价(用户提交请求时，自动生成报价)
    daily_price = Column(Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True)

    # 常驻摄影地
    location_id = Column(Integer, ForeignKey('enum_values.id'), nullable=True)
    location = relationship('EnumValues', backref=backref('users_of_location', uselist=True), foreign_keys=[location_id])

    # 是否接受出差
    accept_travel = db.Column(db.Boolean(), nullable=True)

    @staticmethod
    def type_filter():
        return EnumValues.type_filter(const.USER_TYPE_KEY)

    @staticmethod
    def normal_user_filter():
        # return EnumValues.type_filter(const.NORMAL_USER_TYPE)
        return db.session.query(User).join(EnumValues).filter_by(code=const.NORMAL_USER_TYPE)

    @staticmethod
    def photographer_user_filter():
        return db.session.query(User).join(EnumValues).filter_by(code=const.PHOTOGRAPHER_USER_TYPE)

    # 用户状态, 根据 confirmed_at 字段来动态的获取
    @hybrid_property
    def status(self):
        if self.confirmed_at is None:
            return EnumValues.find_one_by_code(USER_STATUS_UN_VERIFIED)
        return EnumValues.find_one_by_code(USER_STATUS_VERIFIED)

    @status.setter
    def status(self, value):
        pass

    def __repr__(self):
        return self.display

    def __unicode__(self):
        return self.__repr__()

    def __str__(self):
        return self.__repr__()


class UserExperience(db.Model):
    """
    用户的经历
    """
    __tablename__ = 'user_experience'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    # 该经历所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relation("User", backref=backref(
        'experience', uselist=False, cascade='all, delete-orphan'))
