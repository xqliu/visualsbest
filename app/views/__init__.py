# coding=utf-8
from app.models import User, Role
from app.views.admin_index_view import AdminMainView
from app.views.security import RoleAdmin, UserAdmin
from flask.ext.admin import Admin
from flask.ext.admin.consts import ICON_TYPE_GLYPH
from flask.ext.babelex import lazy_gettext


def init_admin_views(app, db):
    db_session = db.session
    admin_views = Admin(app, lazy_gettext('Visual\'s Best'),
                        index_view=AdminMainView(),
                        base_template='layout/admin_layout.html',
                        template_mode='bootstrap3')
    admin_views.add_view(UserAdmin(User, db_session, name=lazy_gettext('User'),
                                  category=u'安全', menu_icon_type=ICON_TYPE_GLYPH,
                                   menu_icon_value='glyphicon-user'))
    admin_views.add_view(RoleAdmin(Role, db_session, name=lazy_gettext("Role"),
                                  category=u'安全', menu_icon_type=ICON_TYPE_GLYPH,
                                   menu_icon_value='glyphicon-eye-close'))

    return admin_views
