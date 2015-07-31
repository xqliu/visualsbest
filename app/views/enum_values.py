# coding=utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.babelex import lazy_gettext


class EnumValuesAdmin(ModelView):
    column_list = ('id', 'code', 'display', 'type')

    column_editable_list = ['display']
    column_searchable_list = ['code', 'display']
    # column_filters = ('code', 'display',)
    column_labels = {
        'id': lazy_gettext('id'),
        'type': lazy_gettext('Type'),
        'code': lazy_gettext('Code'),
        'display': lazy_gettext('Display'),
        'type_values': lazy_gettext('Type Values'),
    }

    form_excluded_columns = ('users_of_type', 'users_of_status', 'orders_of_status')