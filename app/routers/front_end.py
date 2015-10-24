# encoding=utf-8
import datetime
from app import app_provider, const, AppInfo
from app.forms.user_profile_form import UserProfileForm
from app.models import User, EnumValues, \
    PhotoCollection, Request, Order, Message
from app.util import view_util
from app.util.db_util import save_obj_commit
from app.util.photo_collection_util import render_search_result
from app.util.view_util import rt
from flask import request, flash
from flask.ext.login import current_user
from flask.ext.security import login_required
from sqlalchemy import desc

app = app_provider.AppInfo.get_app()
db = AppInfo.get_db()


@app.route("/")
def index():
    all_styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    all_categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    start_date = datetime.datetime.now() + datetime.timedelta(1)
    return rt('index.html', all_styles=all_styles, all_categories=all_categories, start_date=start_date)


@app.route("/photograph", methods=['GET', 'POST'])
def photograph():
    def get_all():
        pg_type = EnumValues.find_one_by_code(const.PHOTOGRAPHER_USER_TYPE)
        photographs = User.query.filter_by(type_id=pg_type.id).all()
        return photographs

    def get_filtered(collections):
        photographs = []
        for c in collections:
            if c.photographer not in photographs:
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
        .order_by(desc(PhotoCollection.date)).all()
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
        else:
            flash('请确保所有必填字段已填写(日拍摄报价为必填字段)')
    return rt('settings.html', user_profile_form=UserProfileForm(), user_styles=user.styles,
              user=user, all_styles=all_styles)
