# encoding=utf-8
import calendar
from datetime import datetime, date, timedelta
from app import app_provider, AppInfo, const
from app.forms.date_status_form import DateStatusForm
from app.forms.photo_collection_form import PhotoCollectionForm
from app.forms.request_service_form import RequestServiceForm
from app.forms.user_profile_form import UserProfileForm
from app.models import User, UserExperience, EnumValues, \
    PhotoCollection, DateStatus
from app.util import view_util
from app.util.db_util import save_obj_commit, delete_by_id
from app.util.photo_collection_util import add_photo_works, delete_photo_works, save_photo_collection, \
    render_search_result
from app.util.view_util import rt
from flask import request, redirect, url_for, flash, jsonify
from flask.ext.login import current_user
from flask.ext.security import login_required
from sqlalchemy import desc, or_, and_

app = app_provider.AppInfo.get_app()


@app.route("/")
def index():
    return rt('index.html')


@app.route("/collection_details/<int:collection_id>")
def collection_details(collection_id):
    collection = PhotoCollection.query.get(collection_id)
    return rt('collection_details.html', collection=collection)


@app.route("/photograph", methods=['GET', 'POST'])
def photograph():
    def get_all():
        pg_type = EnumValues.find_one_by_code('PHOTOGRAPHER_USER')
        photographs = User.query.filter_by(type_id=pg_type.id).all()
        return photographs

    def get_filtered(collections):
        photographs = []
        for c in collections:
            if not c.photographer in photographs:
                photographs.append(c.photographer)
        return photographs

    return render_search_result(template='photograph.html', router='/photograph', get_all=get_all,
                                get_filtered=get_filtered)


@app.route("/works", methods=['GET', 'POST'])
def works():
    def get_all():
        return PhotoCollection.query.filter(PhotoCollection.photos.any()).all()

    def get_filtered(collections):
        return collections

    return render_search_result(template='works.html', router='/works', get_all=get_all, get_filtered=get_filtered)


@app.route("/search")
def search():
    return rt('search.html')


@app.route("/comments")
def comments():
    return rt('comments.html')


@app.route("/edit_collection/<int:collection_id>", methods=['GET', 'POST'])
def edit_collection(collection_id):
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection.query.get(collection_id)
    if photo_collection.photographer != current_user:
        flash('您没有权限编辑本作品集，将返回网站主页')
        return redirect(url_for('index'))
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        if request.form.get('photo-collection-to-delete') is not None \
                and len(request.form.get('photo-collection-to-delete')) != 0:
            id_to_delete = int(request.form.get('photo-collection-to-delete'))
            delete_by_id(PhotoCollection, id_to_delete)
            flash('作品集删除成功')
            return redirect(url_for('my_photos'))
        elif request.form.get('photo-works-to-delete') is not None:
            works_to_delete = request.form.get('photo-works-to-delete').split(',')
            delete_photo_works(works_to_delete)
            files = request.files.getlist('photos[]')
            if not (len(files) == 1 and files[0].filename == u''):
                add_photo_works(files, photo_collection)
        else:
            save_photo_collection(form, photo_collection)
        AppInfo.get_db().session.commit()
    return rt('edit_collection.html', photo_collection=photo_collection, categories=categories, form=form,
              styles=styles)


@app.route("/create_collection", methods=['GET', 'POST'])
@login_required
def create_collection():
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection()
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        if form.validate_on_submit():
            photo_collection.photographer_id = current_user.id
            photo_collection.uploader_id = current_user.id
            save_photo_collection(form, photo_collection)
            save_obj_commit(photo_collection)
            flash('作品集创建成功，您可以在本界面上传作品集中的作品')
            return redirect(url_for('edit_collection', collection_id=photo_collection.id))
        else:
            flash('请填写所有信息并再次尝试创建')
    return rt('create_collection.html', photo_collection=photo_collection, categories=categories, form=form,
              styles=styles)


@app.route("/blog/<int:photographer_id>")
def blog(photographer_id):
    photographer = User.query.get(photographer_id)
    sorted_collections = PhotoCollection.query.filter_by(photographer_id=photographer.id) \
        .order_by(desc(PhotoCollection.date)).all()
    return rt('blog.html', photographer=photographer, collections=sorted_collections)


@app.route("/dashboard")
@login_required
def dashboard():
    return rt('dashboard.html')


@app.route("/my_photos")
@login_required
def my_photos():
    photo_collections = PhotoCollection.query.filter_by(
        photographer_id=current_user.id).all()
    return rt('my_photos.html', photo_collections=photo_collections)


@app.route("/orders")
@login_required
def orders():
    return rt('orders.html')


@app.route("/messages")
@login_required
def messages():
    return rt('messages.html')


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.filter_by(id=current_user.id).first()
    all_styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    if request.method == 'POST':
        form = UserProfileForm()
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
            user.styles = []
            for style_id in form.users_styles.data:
                style = EnumValues.query.get(int(style_id))
                if style is not None:
                    user.styles.append(style)
            if ('photo' in request.files) and \
                    (len(request.files.get('photo').filename) > 0):
                view_util.save_user_gallery(user, request.files['photo'])
            save_obj_commit(user)
    return rt('settings.html', user_profile_form=UserProfileForm(), user_styles=user.styles,
              user=user, all_styles=all_styles)


@app.route('/experience/edit/<int:photographer_id>', methods=['GET', 'POST'])
@login_required
def edit_experience(photographer_id):
    if photographer_id == current_user.id:
        user = User.query.filter_by(id=photographer_id).first()
        exp = user.experience
        if request.method == 'POST':
            if exp is None:
                exp = UserExperience()
            exp.user_id = user.id
            exp.content = request.form['experience-textarea']
            save_obj_commit(exp)
        return rt('edit_experience.html', user_profile_form=UserProfileForm(), experience=exp)
    else:
        flash('您没有权限编辑该用户的摄影经历')
        return redirect(url_for('index'))


@app.route('/experience/<int:photographer_id>', methods=['GET'])
def experience(photographer_id):
    user = User.query.filter_by(id=photographer_id).first()
    exp = user.experience
    return rt('experience.html', user_profile_form=UserProfileForm(), photographer=user, experience=exp)


@app.route('/date_status/json/<int:photographer_id>', methods=['GET'])
def date_status_json(photographer_id):
    year = int(request.args.get('ano'))
    month = int(request.args.get('mes'))
    month_begin = date(year, month, 1)
    month_end = date(year, month, calendar.monthrange(year, month)[1])
    query = AppInfo.get_db().session.query(DateStatus)
    date_statuses = query.filter(DateStatus.user_id == photographer_id) \
        .filter(or_(and_(DateStatus.start_date >= month_begin, DateStatus.start_date <= month_end),
                    and_(DateStatus.end_date >= month_begin, DateStatus.end_date <= month_end))).all()
    events = []
    for ds in date_statuses:
        day_count = (ds.end_date - ds.start_date).days + 1
        for single_date in [d for d in (ds.start_date + timedelta(n) for n in range(day_count)) if d <= ds.end_date]:
            event = dict()
            event['date'] = '{dt.day}/{dt.month}/{dt.year}'.format(dt=single_date)
            event['title'] = u'不可用'
            event['color'] = u'rgba(190, 190, 190, 0.6)'
            event['class'] = u'unavailable'
            events.append(event)
    return jsonify(events=events)


@app.route('/date_status/edit/<int:photographer_id>', methods=['GET', 'POST'])
@login_required
def edit_date_status(photographer_id):
    if photographer_id == current_user.id:
        user = User.query.filter_by(id=photographer_id).first()
        form = DateStatusForm()
        if request.method == 'POST':
            if request.form.get('action') == 'create':
                if form.validate_on_submit():
                    start_date = form.from_day.data
                    end_date = form.end_day.data
                    date_status = DateStatus()
                    date_status.start_date = start_date
                    date_status.end_date = end_date
                    date_status.user_id = photographer_id
                    date_status.status = EnumValues.find_one_by_code('DATE_STATUS_NOT_AVAILABLE')
                    save_obj_commit(date_status)
                    flash('工作日历修改成功')
                else:
                    flash('输入错误，请重新选择起始日期')
            elif request.form.get('action') == 'delete':
                id_to_del = int(request.form.get('id_to_delete'))
                delete_by_id(DateStatus, id_to_del)
                flash('工作日历中不可用时间段删除成功')
        date_statuses = user.date_statuses
        return rt('edit_date_status.html', user_profile_form=UserProfileForm(), form=form, date_statuses=date_statuses)
    else:
        flash('您没有权限编辑该用户的工作日历')
        return redirect(url_for('index'))


@app.route('/request/<int:photographer_id>', methods=['GET'])
@login_required
def request_service(photographer_id):
    user = User.query.filter_by(id=photographer_id).first()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    form = RequestServiceForm(styles)
    return rt('request_service.html', user_profile_form=UserProfileForm(), photographer=user, categories=categories,
              styles=styles, form=form)
