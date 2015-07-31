# coding=utf-8
from app.views.base_view import ModelViewWithAccess
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.babelex import lazy_gettext


class EnumValuesAdmin(ModelViewWithAccess):
    column_list = ('id', 'code', 'display', 'type')

    column_editable_list = ['display']
    column_searchable_list = ['code', 'display']
    column_filters = ('code', 'display',)
    column_labels = {
        'id': u'编号',
        'type': u'类型',
        'code': u'编码',
        'display': u'显示名称',
        'type_values': u'子列表',
    }

    form_excluded_columns = ('users_of_type', 'users_of_status', 'orders_of_status')