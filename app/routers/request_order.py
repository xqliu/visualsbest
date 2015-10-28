# encoding=utf-8
from decimal import Decimal
import datetime

from app import app_provider, const, AppInfo
from app.const import *
from app.forms.request_service_form import RequestServiceForm
from app.models import User, EnumValues, \
    Request, Order, DateStatus, OrderComment, Comment
from app.util.db_util import save_obj_commit, save_objects_commit
from app.util.message_util import create_message, create_request_msg
from app.util.view_util import rt
from flask import request, flash, url_for, redirect, render_template
from flask.ext.login import current_user
from flask.ext.security import login_required

app = app_provider.AppInfo.get_app()
db = AppInfo.get_db()


@app.route("/orders/")
@app.route("/orders/<obj_type>/")
@app.route("/orders/<obj_type>/<status_code>")
@login_required
def orders(obj_type="request", status_code='draft'):
    order_query = db.session.query(Order) \
        .outerjoin(Request, Order.request).outerjoin(EnumValues, Order.status)
    request_query = db.session.query(Request).outerjoin(EnumValues, Request.status)
    if current_user.type.code == const.PHOTOGRAPHER_USER_TYPE:
        order_query = order_query.filter(Request.photographer_id == current_user.id)
        request_query = request_query.filter(Request.photographer_id == current_user.id)
    else:
        order_query = order_query.filter(Request.requester_id == current_user.id)
        request_query = request_query.filter(Request.requester_id == current_user.id)
    if obj_type == 'order':
        all_orders = order_query.filter(EnumValues.code == "ORDER_STATUS_" + status_code.upper()).all()
        requests = request_query.filter(EnumValues.code == const.REQUEST_STATUS_DRAFT).all()
    else:
        requests = request_query.filter(EnumValues.code == "REQUEST_STATUS_" + status_code.upper()).all()
        all_orders = order_query.filter(EnumValues.code == const.ORDER_STATUS_DRAFT).all()
    return rt('orders.html', requests=requests, orders=all_orders)


def check_ownership(obj):
    return obj.requester_id == current_user.id


def check_towards(obj):
    return obj.photographer_id == current_user.id


def check_and_update_request(req, operation_label, status_code, check_func):
    if not check_func(req):
        flash('您没有权限' + operation_label + '本拍摄请求')
        success = False
    elif req.status.code != const.REQUEST_STATUS_DRAFT:
        flash('只能' + operation_label + '处于草稿状态的拍摄请求')
        success = False
    else:
        status = EnumValues.find_one_by_code(status_code)
        req.status = status
        success = True
    return req, success


def mark_order_status(order, check_func, msg, status_code):
    if check_func(order.request):
        status = EnumValues.find_one_by_code(status_code)
        order.status = status
        return order, True
    else:
        flash(msg)
        return order, False


def create_order_from_request(req):
    order = Order()
    order.request_id = req.id
    if req.amount is None:
        order.amount = 0
    else:
        order.amount = req.amount
    draft_order_status = EnumValues.find_one_by_code(const.ORDER_STATUS_DRAFT)
    order.status = draft_order_status
    return order


def create_date_status_from_request(req):
    date_status = DateStatus()
    date_status.start_date = req.start_date
    date_status.end_date = req.end_date
    date_status.status = EnumValues.find_one_by_code(DATE_STATUS_NOT_AVAILABLE)
    date_status.user_id = req.photographer_id
    return date_status


@app.route('/order_comment', methods=['POST'])
def create_order_comment():
    order_id = int(request.form.get('comment_owner_id'))
    order = Order.query.get(order_id)
    if order.request.requester_id == current_user.id and order.status.code == ORDER_STATUS_COMPLETED:
        order_comment = OrderComment()
        comment = Comment()
        comment.user_id = current_user.id
        comment.content = request.form.get('content')
        comment.date = datetime.datetime.now()
        order_comment.comment = comment
        order_comment.order = order
        order_comment.rating = int(request.form.get('rating'))
        status = EnumValues.find_one_by_code(const.ORDER_STATUS_RATED)
        order.status = status
        db.session.add(comment)
        db.session.add(order_comment)
        db.session.add(order)
        content = render_template("message/rate_order.txt", request=order.request, order_comment=order_comment)
        msg = create_message(order.request.requester.id, order.request.photographer.id, content)
        db.session.add(msg)
        db.session.commit()
        flash('拍摄订单服务评价成功')
    else:
        flash('您没有权限评论本订单')
    return redirect(url_for('orders', obj_type='order', status_code='completed'))


@app.route('/order/process', methods=['POST'])
@login_required
def process_order():
    operation = request.form.get('operation')
    order_id = int(request.form.get('order_id'))
    order = Order.query.get(order_id)
    req = order.request
    success = False
    if operation == 'complete':
        order, success = mark_order_status(order, check_ownership, u'只有订单的发起人才可以将该订单标记为完成', ORDER_STATUS_COMPLETED)
        if success:
            create_request_msg(req.requester_id, req.photographer_id, 'message/complete_order.txt', req)
    elif operation == 'confirm_paid':
        order, success = mark_order_status(order, check_towards, u'只有接受订单的摄影师才可以将该订单标记为已付款', ORDER_STATUS_PAID)
        if success:
            create_request_msg(req.photographer_id, req.requester_id, 'message/pay_order.txt', req)
    if success:
        flash(u'更新订单状态成功')
        db.session.add(order)
        db.session.commit()
    return redirect(url_for('orders', obj_type='order'))


@app.route('/request/process', methods=['POST'])
@login_required
def process_request():
    operation = request.form.get('operation')
    request_id = int(request.form.get('request_id'))
    req = Request.query.get(request_id)
    success = False
    if operation == 'cancel':
        req, success = check_and_update_request(req, '取消', REQUEST_STATUS_CANCELLED, check_ownership)
        create_request_msg(req.requester_id, req.photographer_id, 'message/cancel_request.txt', req)
    elif operation == 'confirm':
        req, success = check_and_update_request(req, '确认', REQUEST_STATUS_CONFIRMED, check_towards)
        if success:
            order = create_order_from_request(req)
            db.session.add(order)
            date_status = create_date_status_from_request(req)
            db.session.add(date_status)
            create_request_msg(req.photographer_id, req.requester_id, 'message/confirm_request.txt', req)
    elif operation == 'reject':
        req, success = check_and_update_request(req, '拒绝', REQUEST_STATUS_REJECTED, check_towards)
        create_request_msg(req.photographer_id, req.requester_id, 'message/reject_request.txt', req)
    if success:
        save_obj_commit(req)
        flash('更新拍摄请求状态成功')
    return redirect(url_for('orders'))


@app.route('/request/<int:photographer_id>', methods=['GET', 'POST'])
@login_required
def request_service(photographer_id):
    user = User.query.filter_by(id=photographer_id).first()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    request_obj = Request()
    form = RequestServiceForm(categories, styles)
    if request.method == 'POST':
        if form.validate_on_submit():
            default_status = EnumValues.find_one_by_code(REQUEST_STATUS_DRAFT)
            request_obj.category_id = int(form.category.data)
            request_obj.category = EnumValues.query.get(request_obj.category_id)
            request_obj.style_id = int(form.style.data)
            request_obj.style = EnumValues.query.get(request_obj.style_id)
            request_obj.start_date = form.start_date.data
            request_obj.end_date = form.end_date.data
            request_obj.lens_needed = form.lens_needed.data
            request_obj.requester = current_user
            request_obj.requester_id = current_user.id
            request_obj.photographer_id = int(form.photographer_id.data)
            request_obj.photographer = User.query.get(request_obj.photographer_id)
            request_obj.location = form.location.data
            request_obj.remark = form.remark.data
            request_obj.status = default_status
            request_obj.price = Decimal(form.price.data)
            request_obj.amount = Decimal(form.amount.data)
            content = render_template('message/new_request.txt', request=request_obj)
            message = create_message(request_obj.requester_id, request_obj.photographer_id, content)
            save_objects_commit(request_obj, message)
            flash('创建拍摄请求成功, 转到拍摄请求管理页面')
            return redirect(url_for('orders'))
        else:
            flash('校验失败，请填写所有信息并再次尝试创建拍摄请求(拍摄价格为必填字段)')
            return rt('request_service.html', photographer=user, categories=categories, styles=styles, form=form)
    else:
        return rt('request_service.html', photographer=user, categories=categories, styles=styles, form=form)
