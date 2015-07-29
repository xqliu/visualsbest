# coding=utf-8

from app.app_provider import AppInfo
from flask.ext.security import RoleMixin, UserMixin
from app.models import Image
from sqlalchemy import Column, Integer, ForeignKey
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
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    image = db.relation(Image, backref='image_user')

    # 用户类型
    type_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    type = relationship('EnumValues', backref=backref(
        'users_of_type', uselist=True))

    # 用户状态
    status_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    status = relationship('EnumValues', backref=backref(
        'users_of_status', uselist=True))

    # 该用户是由哪个用户推荐的
    recommend_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recommend_by = db.relation("User", remote_side=id, backref=backref(
        'recommended_users', uselist=True))