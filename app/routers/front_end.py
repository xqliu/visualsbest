# encoding=utf-8
from app import app_provider
from app.forms.user_profile_form import UserProfileForm
from app.models import User, UserExperience
from app.util.db_util import save_obj_commit
from app.util.view_util import render_template_front_layout
from flask import request
from flask.ext.login import current_user
from flask.ext.security import login_required

app = app_provider.AppInfo.get_app()


@app.route("/")
def index():
    return render_template_front_layout('index.html')


@app.route("/works")
def works():
    return render_template_front_layout('works.html')


@app.route("/work_details")
def work_details():
    return render_template_front_layout('work_details.html')


@app.route("/photograph")
def photograph():
    return render_template_front_layout('photograph.html')


@app.route("/search")
def search():
    return render_template_front_layout('search.html')


@app.route("/comments")
def comments():
    return render_template_front_layout('comments.html')


@app.route("/create_collection")
@login_required
def create_collection():
    return render_template_front_layout('create_collection.html')


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
    return render_template_front_layout('my_photos.html')


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
        if request.form['gender'] == '':
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
