# coding=utf-8
from app.views.base_view import ModelViewWithAccess


class OmnibusTemplateAdmin(ModelViewWithAccess):

    column_list = ('id', 'name', 'path')

    form_columns = ('name', 'path',)

    column_labels = {
        'id': u'编号',
        'name': u'模板名称',
        'path': u'模板文件路径(HTML)',
    }
