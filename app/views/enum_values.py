# coding=utf-8
from app.views.base_view import ModelViewWithAccess


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

    form_excluded_columns = (
        'users_of_style', 'users_of_status', 'users_of_type', 'orders_of_status', 'photo_collections_of_style',
        'date_status_of_status', 'request_of_style', 'request_of_category', 'photo_collections_of_category'
    )
