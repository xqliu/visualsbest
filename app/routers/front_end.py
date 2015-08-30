# encoding=utf-8
from app import app_provider, AppInfo, const
from app.forms.photo_collection_form import PhotoCollectionForm
from app.forms.user_profile_form import UserProfileForm
from app.models import User, UserExperience, EnumValues, \
    PhotoCollection
from app.util import view_util
from app.util.db_util import save_obj_commit
from app.util.photo_collection_util import add_photo_works, delete_photo_works, save_photo_collection, \
    render_search_result
from app.util.view_util import render_template_front_layout
from flask import request, redirect, url_for, flash
from flask.ext.login import current_user
from flask.ext.security import login_required
from sqlalchemy import or_, desc

app = app_provider.AppInfo.get_app()


@app.route("/")
def index():
    return render_template_front_layout('index.html')


@app.route("/collection_details/<int:collection_id>")
def collection_details(collection_id):
    collection = PhotoCollection.query.get(collection_id)
    return render_template_front_layout('collection_details.html', collection=collection)


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

    flash("这是一条我也不知道干什么用的提示信息")
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
    return render_template_front_layout('search.html')


@app.route("/comments")
def comments():
    return render_template_front_layout('comments.html')


@app.route("/edit_collection/<int:collection_id>", methods=['GET', 'POST'])
def edit_collection(collection_id):
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection.query.get(collection_id)
    if photo_collection.photographer != current_user:
        flash('您没有权限编辑本作品集，将返回网站主页')
        return url_for('index')
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        if request.form.get('photo-collection-to-delete') is not None \
                and len(request.form.get('photo-collection-to-delete')) != 0:
            id_to_delete = int(request.form.get('photo-collection-to-delete'))
            pc = PhotoCollection.query.get(id_to_delete)
            AppInfo.get_db().session.delete(pc)
            AppInfo.get_db().session.commit()
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
            flash('作品集创建成功，您可以在本界面上传作品集中的作品')
            return redirect(url_for('edit_collection', collection_id=photo_collection.id))
        else:
            flash('请填写所有信息并再次尝试创建')
    return render_template_front_layout('create_collection.html',
                                        photo_collection=photo_collection,
                                        categories=categories, form=form, styles=styles)


@app.route("/blog/<int:photographer_id>")
def blog(photographer_id):
    photographer = User.query.get(photographer_id)
    sorted_collections = PhotoCollection.query.filter_by(photographer_id=photographer.id) \
        .order_by(desc(PhotoCollection.date)).all()
    return render_template_front_layout('blog.html', photographer=photographer, collections=sorted_collections)


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
            user.styles = []
            for style_id in form.users_styles.data:
                style = EnumValues.query.get(int(style_id))
                if style is not None:
                    user.styles.append(style)
            if ('photo' in request.files) and \
                    (len(request.files.get('photo').filename) > 0):
                view_util.save_user_gallery(user, request.files['photo'])
            save_obj_commit(user)
    return render_template_front_layout('settings.html', user_profile_form=UserProfileForm(), user_styles=user.styles,
                                        user=user, all_styles=all_styles)


@app.route('/experience/edit/<int:photographer_id>', methods=['GET', 'POST'])
@login_required
def edit_experience(photographer_id):
    user = User.query.filter_by(id=photographer_id).first()
    exp = user.experience
    if photographer_id == current_user.id:
        if request.method == 'POST':
            if exp is None:
                exp = UserExperience()
            exp.user_id = user.id
            exp.content = request.form['content']
            save_obj_commit(exp)
        return render_template_front_layout('edit_experience.html', user_profile_form=UserProfileForm(), experience=exp)
    else:
        flash('您没有权限编辑该用户的摄影经理')
        return url_for('index')


@app.route('/experience/<int:photographer_id>', methods=['GET'])
def experience(photographer_id):
    user = User.query.filter_by(id=photographer_id).first()
    exp = user.experience
    return render_template_front_layout('experience.html', user_profile_form=UserProfileForm(), experience=exp)
