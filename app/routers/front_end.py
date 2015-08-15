# encoding=utf-8
from app import app_provider, AppInfo, const
from app.forms.photo_collection_form import PhotoCollectionForm
from app.forms.user_profile_form import UserProfileForm
from app.models import User, UserExperience, PhotoCategory, EnumValues, \
    PhotoCollection, PhotoWork, Image
from app.util import view_util
from app.util.db_util import save_obj_commit
from app.util.view_util import render_template_front_layout
from flask import request, redirect, url_for
from flask.ext.login import current_user
from flask.ext.security import login_required

app = app_provider.AppInfo.get_app()


@app.route("/")
def index():
    return render_template_front_layout('index.html')


@app.route("/works")
def works():
    collections = PhotoCollection.query.all()
    return render_template_front_layout('works.html',
                                        collections=collections)


@app.route("/collection_details/<int:collection_id>")
def collection_details(collection_id):
    collection = PhotoCollection.query.get(collection_id)
    return render_template_front_layout('collection_details.html',
                                        collection=collection)


@app.route("/photograph")
def photograph():
    type = EnumValues.find_one_by_code('PHOTOGRAPHER_USER')
    photographs = User.query.filter_by(type_id=type.id).all()
    return render_template_front_layout('photograph.html',
                                        photographs=photographs)


@app.route("/search")
def search():
    return render_template_front_layout('search.html')


@app.route("/comments")
def comments():
    return render_template_front_layout('comments.html')


@app.route("/edit_collection/<int:collection_id>", methods=['GET', 'POST'])
def edit_collection(collection_id):
    categories = PhotoCategory.query.filter_by(
        photographer_id=current_user.id).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection.query.get(collection_id)
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        works_to_delete = request.form['photo-works-to-delete'].split(',')
        if not (len(works_to_delete) == 1 and works_to_delete[0] == u''):
            for work_id in works_to_delete:
                work = PhotoWork.query.filter_by(id=int(work_id)).first()
                PhotoWork.query.filter_by(id=work_id).delete()
                Image.query.filter_by(id=work.image.id).delete()
        files = request.files.getlist('photos[]')
        if not (len(files) == 1 and files[0].filename == u''):
            for img in files:
                work = PhotoWork()
                work.photo_collection_id = photo_collection.id
                view_util.save_photo_work_image(work, img)
                AppInfo.get_db().session.add(work)
        AppInfo.get_db().session.commit()
    return render_template_front_layout('edit_collection.html',
                                        photo_collection=photo_collection,
                                        categories=categories,
                                        form=form, styles=styles)


@app.route("/create_collection", methods=['GET', 'POST'])
@login_required
def create_collection():
    categories = PhotoCategory.query.filter_by(
        photographer_id=current_user.id).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection()
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        if form.validate_on_submit():
            photo_collection.photographer_id = current_user.id
            photo_collection.uploader_id = current_user.id
            photo_collection.category_id = int(form.category.data)
            photo_collection.style_id = int(form.style.data)
            photo_collection.name = form.name.data
            photo_collection.introduce = form.introduce.data
            save_obj_commit(photo_collection)
            return redirect(url_for('edit_collection',
                                    collection_id=photo_collection.id))
    return render_template_front_layout('create_collection.html',
                                        photo_collection=photo_collection,
                                        categories=categories,
                                        form=form, styles=styles)


@app.route("/photo_categories", methods=['GET', 'POST'])
@login_required
def photo_categories():
    if request.method == 'POST':
        category = None
        if request.form.get('operation') == u'create':
            category = PhotoCategory()
            category.name = request.form.get('name')
            category.photographer_id = current_user.id
        elif request.form.get('operation') == u'edit':
            category_id = request.form.get('id')
            category = PhotoCategory.query.get(int(category_id))
            category.name = request.form.get('name')
        elif request.form.get('operation') == u'delete':
            category_id = int(request.form.get('id'))
            PhotoCategory.query.filter_by(id=category_id).delete()
            AppInfo.get_db().session.commit()
        if category is not None:
            save_obj_commit(category)
    categories = PhotoCategory.query.filter_by(
        photographer_id=current_user.id).all()
    return render_template_front_layout('photo_categories.html',
                                        categories=categories)


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
