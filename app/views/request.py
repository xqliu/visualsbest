# coding=utf-8
from app.models import User, Request
from app.util.view_util import default_date_formatter
from app.views.base_view import ModelViewWithAccess


class RequestAdmin(ModelViewWithAccess):
    form_columns = ('requester', 'photographer', 'style', 'category', 'start_date', 'end_date', 'status', 'style', 'location',
                    'lens_needed', 'price', 'amount', 'remark')

    column_labels = {
        'requester': u'请求用户',
        'photographer': u'请求摄像师',
        'start_date': u'拍摄开始时间',
        'end_date': u'拍摄结束时间',
        'status': u'请求状态',
        'style': u'拍摄风格',
        'category': u'拍摄分类',
        'location': u'拍摄地点',
        'lens_needed': u'所需镜头类型',
        'remark': u'备注',
        'price': u'价格',
        'amount': u'总金额'
    }

    form_args = dict(
        requester=dict(query_factory=User.normal_user_filter),
        photographer=dict(query_factory=User.photographer_user_filter),
        category=dict(query_factory=Request.category_filter),
        style=dict(query_factory=Request.style_filter),
        status=dict(query_factory=Request.status_filter),
    )

    column_formatters = {
        'start_date': default_date_formatter,
        'end_date': default_date_formatter
    }
