# coding=utf-8
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.babelex import lazy_gettext


def init_admin_views(app, db):
    db_session = db.session
    admin_views = Admin(app, lazy_gettext('Brand Name'),
                        index_view=AdminIndexView(),
                        base_template='layout.html',
                        template_mode='bootstrap3')
    return admin_views
