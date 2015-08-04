# coding=utf-8
from app.views.base_view import ModelViewWithAccess


class RequestAdmin(ModelViewWithAccess):
    form_columns = ('requester', 'photographer', 'start_date', 'end_date',
                    'status', 'style', 'location', 'lens_needed',)

    column_labels = {
        'requester': u'请求用户',
        'photographer': u'请求摄像师',
        'start_date': u'拍摄开始时间',
        'end_date': u'拍摄结束时间',
        'status': u'请求状态',
        'style': u'拍摄风格',
        'location': u'拍摄地点',
        'lens_needed': u'所需镜头类型',
    }
