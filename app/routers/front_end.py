# encoding=utf-8
import datetime
from app import app_provider, const, AppInfo
from app.forms.normal_user_profile_form import NormalUserProfileForm
from app.forms.photographer_profile_form import PhotographerProfileForm
from app.models import User, EnumValues, \
    PhotoCollection, Request, OmnibusTemplate, PhotoOmnibus
from app.util import view_util
from app.util.db_util import save_obj_commit
from app.util.photo_collection_util import query_for_photo_collection, extra_fields_from_form
from app.util.view_util import rt
from flask import request, flash
from flask.ext.login import current_user
from flask.ext.security import login_required
from sqlalchemy import or_

app = app_provider.AppInfo.get_app()
db = AppInfo.get_db()


@app.route("/")
def index():
    all_styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    all_categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    start_date = datetime.datetime.now() + datetime.timedelta(1)
    photo_omnibuses = PhotoOmnibus.query.all()
    return rt('index.html', all_styles=all_styles, all_categories=all_categories, start_date=start_date, photo_omnibuses=photo_omnibuses)


@app.route("/photograph", methods=['GET', 'POST'])
def photograph():
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    category, style, include_none_date, include_none_price, min_price, max_price, min_date, max_date = \
        [None, None, None, None, None, None, None, None]
    if request.method == 'POST':
        category_id, include_none_date, include_none_price, max_date, max_price, min_date, min_price, style_id = extra_fields_from_form()
        collections, category, style = query_for_photo_collection(category_id, True, True, None, None, None, None, style_id)

        query = AppInfo.get_db().session.query(User).join(PhotoCollection, User.id == PhotoCollection.photographer_id)
        category, style = None, None
        if category_id is not None:
            query = query.filter(PhotoCollection.category_id == category_id)
            category = EnumValues.query.get(category_id)
        if style_id is not None:
            query = query.filter(PhotoCollection.style_id == style_id)
            style = EnumValues.query.get(style_id)
        if min_price is not None:
            if include_none_price:
                query = query.filter(or_(PhotoCollection.price >= min_price, PhotoCollection.price.is_(None)))
            else:
                query = query.filter(PhotoCollection.price >= min_price)
        if max_price is not None:
            if include_none_price:
                query = query.filter(or_(PhotoCollection.price <= max_price, PhotoCollection.price.is_(None)))
            else:
                query = query.filter(PhotoCollection.price <= max_price)
        if min_date is not None:
            if include_none_date:
                query = query.filter(or_(PhotoCollection.date >= min_date, PhotoCollection.date.is_(None)))
            else:
                query = query.filter(PhotoCollection.date >= min_date)
        if max_date is not None:
            if include_none_date:
                query = query.filter(or_(PhotoCollection.date <= max_date, PhotoCollection.date.is_(None)))
            else:
                query = query.filter(PhotoCollection.date <= max_date)
        collections = query.filter(PhotoCollection.photos.any()).all()

        result_list = []
        for c in collections:
            if c.photographer not in result_list:
                result_list.append(c.photographer)
    else:
        pg_type = EnumValues.find_one_by_code(const.PHOTOGRAPHER_USER_TYPE)
        result_list = User.query.filter_by(type_id=pg_type.id).all()
    return rt("photograph.html", result_list=result_list, categories=categories,
              styles=styles, category=category, style=style, route='/photograph',
              min_price=min_price, max_price=max_price, include_none_price=include_none_price,
              min_date=min_date, max_date=max_date, include_none_date=include_none_date)


@app.route("/works", methods=['GET', 'POST'])
def works():
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    category, style, include_none_date, include_none_price, min_price, max_price, min_date, max_date = \
        [None, None, None, None, None, None, None, None]
    if request.method == 'POST':
        category_id, include_none_date, include_none_price, max_date, max_price, min_date, min_price, style_id = \
            extra_fields_from_form()
        result_list, category, style = query_for_photo_collection(category_id, include_none_date, include_none_price,
                                                                  max_date, max_price, min_date, min_price, style_id)
        min_date = request.form.get('min_date')
        max_date = request.form.get('max_date')
    else:
        result_list = PhotoCollection.query.filter(PhotoCollection.photos.any()).all()
    return rt("works.html", result_list=result_list, categories=categories,
              styles=styles, category=category, style=style, route='/works',
              min_price=min_price, max_price=max_price, include_none_price=include_none_price,
              min_date=min_date, max_date=max_date, include_none_date=include_none_date)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        return rt('search.html')


@app.route("/comments")
def comments():
    return rt('comments.html')


@app.route("/blog/<int:photographer_id>")
def blog(photographer_id):
    photographer = User.query.get(photographer_id)
    sorted_collections = PhotoCollection.query.filter_by(photographer_id=photographer.id) \
        .order_by(PhotoCollection.date.desc()).all()
    return rt('blog.html', photographer=photographer, collections=sorted_collections)


@app.route("/dashboard")
@login_required
def dashboard():
    request_query = db.session.query(Request).outerjoin(EnumValues, Request.status)
    if current_user.type.code == const.PHOTOGRAPHER_USER_TYPE:
        draft_requests = request_query.filter(Request.photographer_id == current_user.id) \
            .filter(EnumValues.code == const.REQUEST_STATUS_DRAFT).all()
    else:
        draft_requests = request_query.filter(Request.requester_id == current_user.id) \
            .filter(EnumValues.code == const.REQUEST_STATUS_DRAFT).all()
    return rt('dashboard.html', draft_requests=draft_requests)


@app.route("/my_photos")
@login_required
def my_photos():
    photo_collections = PhotoCollection.query.filter_by(
        photographer_id=current_user.id).all()
    return rt('my_photos.html', photo_collections=photo_collections)


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.filter_by(id=current_user.id).first()
    all_locations = EnumValues.type_filter(const.LOCATION_TYPE_KEY).all()
    if current_user.type.code == const.PHOTOGRAPHER_USER_TYPE:
        form = PhotographerProfileForm()
    else:
        form = NormalUserProfileForm()
    if request.method == 'POST':
        if request.form.get('gender') is None \
                or request.form.get('gender') == '':
            form.gender.data = u'保密'
        if form.validate_on_submit():
            user.login = form.login.data
            user.display = form.display.data
            user.gender = form.gender.data
            user.birthday = form.birthday.data
            user.mobile_phone = form.mobile_phone.data
            user.email = form.email.data
            user.weibo_account = form.weibo_account.data
            user.wechat_account = form.wechat_account.data
            user.qq_number = form.qq_number.data
            user.introduce = form.introduce.data
            user.daily_price = form.daily_price.data
            user.accept_travel = form.accept_travel.data
            user.location_id = int(form.location.data)
            if ('photo' in request.files) and \
                    (len(request.files.get('photo').filename) > 0):
                view_util.save_user_gallery(user, request.files['photo'])
            save_obj_commit(user)
            flash('更新个人信息成功！')
        else:
            flash('请确保所有必填字段已填写(日拍摄报价为必填字段)')
    return rt('settings.html', user_profile_form=form, user=user, all_locations=all_locations)
