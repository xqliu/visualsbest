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
from flask import request, redirect, url_for
from flask.ext.login import current_user
from flask.ext.security import login_required

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

    return render_search_result(template='photograph.html', router='/photograph', get_all=get_all,
                                get_filtered=get_filtered)


@app.route("/works", methods=['GET', 'POST'])
def works():
    def get_all():
        return PhotoCollection.query.all()

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
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        if request.form.get('photo-works-to-delete') is not None:
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
    return render_template_front_layout('settings.html',
                                        user_profile_form=UserProfileForm(),
                                        user_styles=user.styles, user=user, all_styles=all_styles)


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
