# coding=utf-8
from app.views.base_view import ModelViewWithAccess
from flask.ext.admin.model import InlineFormAdmin
from app.models.photo_work import PhotoWorkOmnibus


class PhotoWorkInlineAdmin(InlineFormAdmin):
    form_args = dict(
        photo_work=dict(label=u'作品'),
        work_row=dict(label=u'行', description=u'该作品在主推作品集中显示的行'),
        work_col=dict(label=u'列', description=u'该作品在主推作品集中显示的列'),
    )


class PhotoOmnibusAdmin(ModelViewWithAccess):
    inline_models = (PhotoWorkInlineAdmin(PhotoWorkOmnibus),)

    form_columns = ('template', 'photo_works',)

    column_labels = {
        'template': u'主推模板',
        'photo_works': u'主推作品列表',
    }
