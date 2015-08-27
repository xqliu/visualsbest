# encoding=utf-8
from datetime import datetime
from app import app_provider, AppInfo, const
from app.forms.photo_collection_form import PhotoCollectionForm
from app.forms.user_profile_form import UserProfileForm
from app.models import User, UserExperience, EnumValues, \
    PhotoCollection
from app.util import view_util
from app.util.db_util import save_obj_commit
from app.util.photo_collection_util import add_photo_works, delete_photo_works, save_photo_collection, \
    query_for_photo_collection
from app.util.view_util import render_template_front_layout
from boto.mturk import price
from flask import request, redirect, url_for
from flask.ext.login import current_user
from flask.ext.security import login_required
from sqlalchemy import or_

app = app_provider.AppInfo.get_app()


@app.route("/")
def index():
    return render_template_front_layout('index.html')


@app.route("/works", methods=['GET', 'POST'])
def works():
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    category, style, include_none_date, include_none_price, min_price, max_price, min_date, max_date = \
        [None, None, None, None, None, None, None, None]
    if request.method == 'POST':
        category_id = int(request.form.get('category_id')) if len(request.form.get('category_id')) > 0 else None
        style_id = int(request.form.get('style_id')) if len(request.form.get('style_id')) > 0 else None
        min_price = int(request.form.get('min_price')) if len(request.form.get('min_price')) > 0 else None
        max_price = int(request.form.get('max_price')) if len(request.form.get('max_price')) > 0 else None
        min_date = datetime.strptime(request.form.get('min_date'), '%Y-%m-%d') \
            if len(request.form.get('min_date')) > 0 else None
        max_date = datetime.strptime(request.form.get('max_date'), '%Y-%m-%d') \
            if len(request.form.get('max_date')) > 0 else None
        include_none_price = request.form.get('include_none_price')
        include_none_date = request.form.get('include_none_date')
        collections, category, style = query_for_photo_collection(category_id, include_none_date, include_none_price,
                                                                  max_date, max_price, min_date, min_price, style_id)
        min_date = request.form.get('min_date')
        max_date = request.form.get('max_date')
    else:
        collections = PhotoCollection.query.all()
    return render_template_front_layout('works.html', collections=collections,
                                        categories=categories, styles=styles, category=category, style=style,
                                        min_price=min_price, max_price=max_price, include_none_price=include_none_price,
                                        min_date=min_date, max_date=max_date, include_none_date=include_none_date)


@app.route("/collection_details/<int:collection_id>")
def collection_details(collection_id):
    collection = PhotoCollection.query.get(collection_id)
    return render_template_front_layout('collection_details.html', collection=collection)


@app.route("/photograph")
def photograph():
    type = EnumValues.find_one_by_code('PHOTOGRAPHER_USER')
    photographs = User.query.filter_by(type_id=type.id).all()
    return render_template_front_layout('photograph.html', photographs=photographs)


@app.route("/search")
def search():
    return render_template_front_layout('search.html')


@app.route("/comments")
def comments():
    return render_template_front_layout('comments.html')


@app.route("/edit_collection/<int:collection_id>", methods=['GET', 'POST'])
def edit_collection(collection_id):
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection.query.get(collection_id)
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        works_to_delete = []
        if request.form.get('photo-works-to-delete') is not None:
            works_to_delete = request.form.get('photo-works-to-delete').split(',')
        delete_photo_works(works_to_delete)
        files = request.files.getlist('photos[]')
        if not (len(files) == 1 and files[0].filename == u''):
            add_photo_works(files, photo_collection)
        save_photo_collection(form, photo_collection)
        AppInfo.get_db().session.commit()
    return render_template_front_layout('edit_collection.html',
                                        photo_collection=photo_collection,
                                        categories=categories,
                                        form=form, styles=styles)


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
            return redirect(url_for('edit_collection',
                                    collection_id=photo_collection.id))
    return render_template_front_layout('create_collection.html',
                                        photo_collection=photo_collection,
                                        categories=categories,
                                        form=form, styles=styles)


@app.route("/blog")
def blog():
    return render_template_front_layout('blog.html')


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template_front_layout('dashboard.html')


@app.route("/my_photos")
@login_required
def my_photos():
    photo_collections = PhotoCollection.query.filter_by(
        photographer_id=current_user.id).all()
    return render_template_front_layout('my_photos.html',
                                        photo_collections=photo_collections)


@app.route("/orders")
@login_required
def orders():
    return render_template_front_layout('orders.html')


@app.route("/messages")
@login_required
def messages():
    return render_template_front_layout('messages.html')


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.filter_by(id=current_user.id).first()
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
            if ('photo' in request.files) and \
                    (len(request.files.get('photo').filename) > 0):
                view_util.save_user_gallery(user, request.files['photo'])
            save_obj_commit(user)
    return render_template_front_layout('settings.html',
                                        user_profile_form=UserProfileForm(),
                                        user=user)


@app.route('/experience', methods=['GET', 'POST'])
@login_required
def experience():
    user = User.query.filter_by(id=current_user.id).first()
    exp = user.experience
    if request.method == 'POST':
        if exp is None:
            exp = UserExperience()
        exp.user_id = user.id
        exp.content = request.form['content']
        save_obj_commit(exp)
    return render_template_front_layout('experience.html',
                                        user_profile_form=UserProfileForm(),
                                        experience=exp)
