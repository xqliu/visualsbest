# coding=utf-8

from app.app_provider import AppInfo
from flask.ext.security import RoleMixin, UserMixin
from image import Image
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()

roles_users = db.Table('roles_users',
                       db.Column('id', db.Integer(), primary_key=True),
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    login = db.Column(db.String(64), unique=True, nullable=False)
    display = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    mobile_phone = db.Column(db.String(16), nullable=False)
    qq_number = db.Column(db.String(16), nullable=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    image = db.relation(Image, backref='image_user')

    # 用户类型
    type_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    type = relationship('EnumValues', backref=backref(
        'users_of_type', uselist=True), foreign_keys=[type_id])

    # 用户状态
    status_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    status = relationship('EnumValues', backref=backref(
        'users_of_status', uselist=True), foreign_keys=[status_id])

    # 该用户是由哪个用户推荐的
    recommend_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recommend_by = db.relation("User", remote_side=id, backref=backref(
        'recommended_users', uselist=True))

    confirmed_at = Column(DateTime, nullable=True)


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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relation("User", backref=backref(
        'experience', uselist=False, cascade='all, delete-orphan'))
