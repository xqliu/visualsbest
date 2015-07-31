# coding=utf-8
from app.models import User, Role, EnumValues
from app.views.admin_index_view import AdminMainView
from app.views.enum_values import EnumValuesAdmin
from app.views.security import RoleAdmin, UserAdmin
from flask.ext.admin import Admin
from flask.ext.admin.consts import ICON_TYPE_GLYPH
from flask.ext.babelex import lazy_gettext


def init_admin_views(app, db):
    db_session = db.session
    admin_views = Admin(app, lazy_gettext(u'Visual\'s Best 管理后台'),
                        index_view=AdminMainView(),
                        base_template='layout/admin_layout.html',
                        template_mode='bootstrap3')
    admin_views.add_view(UserAdmin(User, db_session, name=u'用户', menu_icon_type=ICON_TYPE_GLYPH,
                                   menu_icon_value='glyphicon-user'))
    admin_views.add_view(RoleAdmin(Role, db_session, name=u'角色', menu_icon_type=ICON_TYPE_GLYPH,
                                   menu_icon_value='glyphicon-eye-close'))
    admin_views.add_view(EnumValuesAdmin(EnumValues, db_session, name=u'列表设定', menu_icon_type=ICON_TYPE_GLYPH,
                                         menu_icon_value='glyphicon-tasks'))
    return admin_views
