# coding=utf-8
from app.models import User, Role, EnumValues, Order, Request, PhotoOmnibus, OmnibusTemplate
from app.views.admin_index_view import AdminMainView
from app.views.enum_values import EnumValuesAdmin
from app.views.order import OrderAdmin
from app.views.request import RequestAdmin
from app.views.security import RoleAdmin, UserAdmin
from app.views.photo_omnibus import PhotoOmnibusAdmin
from app.views.omnibus_template import OmnibusTemplateAdmin
from flask.ext.admin import Admin
from flask.ext.admin.consts import ICON_TYPE_GLYPH
from flask.ext.babelex import lazy_gettext


def init_admin_views(app, db):
    db_session = db.session
    admin_views = Admin(app, lazy_gettext(u'Visual\'s Best 管理后台'),
                        index_view=AdminMainView(),
                        base_template='layout/admin_layout.html',
                        template_mode='bootstrap3')
    admin_views.add_view(RequestAdmin(Request, db_session, name=u'拍摄请求', menu_icon_type=ICON_TYPE_GLYPH,
                                      category=u'订单相关', menu_icon_value='glyphicon-inbox'))
    admin_views.add_view(OrderAdmin(Order, db_session, name=u'订单', menu_icon_type=ICON_TYPE_GLYPH,
                                    category=u'订单相关', menu_icon_value='glyphicon-shopping-cart'))
    admin_views.add_view(OmnibusTemplateAdmin(OmnibusTemplate, db_session, name=u'主推模板', menu_icon_type=ICON_TYPE_GLYPH,
                                              category=u'主推', menu_icon_value='glyphicon-th'))
    admin_views.add_view(PhotoOmnibusAdmin(PhotoOmnibus, db_session, name=u'主推作品', menu_icon_type=ICON_TYPE_GLYPH,
                                           category=u'主推', menu_icon_value='glyphicon-star'))
    admin_views.add_view(UserAdmin(User, db_session, name=u'用户', menu_icon_type=ICON_TYPE_GLYPH,
                                   category=u'用户相关', menu_icon_value='glyphicon-user'))
    admin_views.add_view(RoleAdmin(Role, db_session, name=u'角色', menu_icon_type=ICON_TYPE_GLYPH,
                                   category=u'用户相关', menu_icon_value='glyphicon-eye-close'))
    admin_views.add_view(EnumValuesAdmin(EnumValues, db_session, name=u'列表设定', menu_icon_type=ICON_TYPE_GLYPH,
                                         category=u'系统设定', menu_icon_value='glyphicon-tasks'))
    return admin_views
