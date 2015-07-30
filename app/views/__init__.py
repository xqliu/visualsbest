# coding=utf-8
from app.views.admin_index_view import AdminMainView
from flask.ext.admin import Admin
from flask.ext.babelex import lazy_gettext


def init_admin_views(app, db):
    db_session = db.session
    admin_views = Admin(app, lazy_gettext('Visual\'s Best'),
                        index_view=AdminMainView(),
                        base_template='layout/admin_layout.html',
                        template_mode='bootstrap3')
    return admin_views
