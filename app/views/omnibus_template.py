# coding=utf-8
from app.views.base_view import ModelViewWithAccess
from flask.ext.admin.model import InlineFormAdmin
from flask.ext.admin.contrib.sqla import ModelView
from app.models.order import OrderComment
from flask.ext.babelex import lazy_gettext


class OmnibusTemplateAdmin(ModelViewWithAccess):

    column_list = ('id', 'name', 'path')

    form_columns = ('name', 'path',)

    column_labels = {
        'id': u'编号',
        'name': u'模板名称',
        'path': u'模板文件路径(HTML)',
    }
