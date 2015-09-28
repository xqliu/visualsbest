# coding=utf-8
from app.models import Request, Order
from app.views.base_view import ModelViewWithAccess
from flask.ext.admin.model import InlineFormAdmin
from app.models.order import OrderComment


class OrderCommentsInlineAdmin(InlineFormAdmin):
    form_args = dict(
        comment=dict(label=u'关联评论'),
        rating=dict(label=u'评分')
    )


class OrderAdmin(ModelViewWithAccess):
    form_columns = ('request', 'status', 'amount')

    column_labels = {
        'request': u'关联拍摄请求',
        'status': u'订单状态',
        'order_comments': u'订单评论',
        'amount': u'价格总金额',
    }

    form_args = dict(
        request=dict(query_factory=Request.draft_status_filter, description=u'本处只列出了处于未确认状态的拍摄请求'),
        status=dict(query_factory=Order.status_filter)
    )
