# encoding=utf-8
from decimal import Decimal
from app import app_provider, const, AppInfo
from app.const import REQUEST_STATUS_DRAFT
from app.forms.request_service_form import RequestServiceForm
from app.forms.user_profile_form import UserProfileForm
from app.models import User, EnumValues, \
    Request, Order
from app.util.db_util import save_obj_commit
from app.util.view_util import rt
from flask import request, flash, url_for, redirect
from flask.ext.login import current_user
from flask.ext.security import login_required

app = app_provider.AppInfo.get_app()


@app.route("/orders/")
@app.route("/orders/<obj_type>/")
@app.route("/orders/<obj_type>/<status_code>")
@login_required
def orders(obj_type="request", status_code='draft'):
    order_query = AppInfo.get_db().session.query(Order) \
        .outerjoin(Request, Order.request).outerjoin(EnumValues, Order.status)
    request_query = AppInfo.get_db().session.query(Request).outerjoin(EnumValues, Request.status)
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


def check_and_update_coming_request(req, operation_label, status_code, check_function):
    if not check_function(req):
        flash('您没有权限' + operation_label + '本拍摄请求')
    elif req.status.code != const.REQUEST_STATUS_DRAFT:
        flash('只能' + operation_label + '处于草稿状态的拍摄请求')
    else:
        status = EnumValues.find_one_by_code(status_code)
        req.status = status
    return req


@app.route('/order/process', methods=['POST'])
@login_required
def process_order():
    operation = request.form.get('operation')
    order_id = int(request.form.get('order_id'))
    order = Order.query.get(order_id)
    if operation == 'complete':
        if order.request.requester_id == current_user.id:
            status = EnumValues.find_one_by_code(const.ORDER_STATUS_COMPLETE)
            order.status = status
            save_obj_commit(order)
        else:
            flash("只有订单的发起人才可以将该订单标记为完成")
    all_orders, requests = get_requests_orders()
    return rt('orders.html', requests=requests, orders=all_orders)


@app.route('/request/process', methods=['POST'])
@login_required
def process_request():
    def check_ownership(obj):
        return obj.requester_id == current_user.id

    def check_towards(obj):
        return obj.photographer_id == current_user.id

    operation = request.form.get('operation')
    request_id = int(request.form.get('request_id'))
    req = Request.query.get(request_id)
    if operation == 'cancel':
        req = check_and_update_coming_request(req, '确认', const.REQUEST_STATUS_CONFIRMED, check_ownership)
    elif operation == 'confirm':
        req = check_and_update_coming_request(req, '确认', const.REQUEST_STATUS_CONFIRMED, check_towards)
        order = Order()
        order.request_id = req.id
        if req.amount is None:
            order.amount = 0
        else:
            order.amount = req.amount
        draft_order_status = EnumValues.find_one_by_code(const.ORDER_STATUS_DRAFT)
        order.status = draft_order_status
        save_obj_commit(order)
    elif operation == 'reject':
        req = check_and_update_coming_request(req, '拒绝', const.REQUEST_STATUS_REJECTED, check_towards)
    save_obj_commit(req)
    all_orders, requests = get_requests_orders()
    return rt('orders.html', requests=requests, orders=all_orders)


def get_requests_orders():
    order_query = AppInfo.get_db().session.query(Order).outerjoin(Request, Order.request) \
        .outerjoin(EnumValues, Order.status)
    request_query = AppInfo.get_db().session.query(Request).outerjoin(EnumValues, Request.status)
    order_query = order_query.filter(Request.requester_id == current_user.id)
    request_query = request_query.filter(Request.requester_id == current_user.id)
    requests = request_query.filter(EnumValues.code == const.REQUEST_STATUS_DRAFT).all()
    all_orders = order_query.filter(EnumValues.code == const.ORDER_STATUS_DRAFT).all()
    return all_orders, requests


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
            request_obj.style_id = int(form.style.data)
            request_obj.start_date = form.start_date.data
            request_obj.end_date = form.end_date.data
            request_obj.lens_needed = form.lens_needed.data
            request_obj.requester_id = current_user.id
            request_obj.photographer_id = int(form.photographer_id.data)
            request_obj.location = form.location.data
            request_obj.remark = form.remark.data
            request_obj.status = default_status
            request_obj.price = Decimal(form.price.data)
            request_obj.amount = Decimal(form.amount.data)
            save_obj_commit(request_obj)
            flash('创建拍摄请求成功, 转到拍摄请求管理页面')
            return redirect(url_for('orders'))
        else:
            flash('校验失败，请填写所有信息并再次尝试创建拍摄请求')
            return rt('request_service.html', user_profile_form=UserProfileForm(), photographer=user,
                      categories=categories, styles=styles, form=form)
    else:
        return rt('request_service.html', user_profile_form=UserProfileForm(), photographer=user,
                  categories=categories, styles=styles, form=form)
