# encoding=utf-8
from app import app_provider
from app.views.app_util import render_template_with_frontend_layout
from flask.ext.security import login_required

app = app_provider.AppInfo.get_app()


@app.route("/")
def index():
    return render_template_with_frontend_layout('index.html')


@app.route("/works")
def works():
    return render_template_with_frontend_layout('works.html')


@app.route("/work_details")
def work_details():
    return render_template_with_frontend_layout('work_details.html')


@app.route("/photograph")
def photograph():
    return render_template_with_frontend_layout('photograph.html')


@app.route("/search")
def search():
    return render_template_with_frontend_layout('search.html')


@app.route("/comments")
def comments():
    return render_template_with_frontend_layout('comments.html')


@app.route("/create_collection")
@login_required
def create_collection():
    return render_template_with_frontend_layout('create_collection.html')


@app.route("/blog")
def blog():
    return render_template_with_frontend_layout('blog.html')


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template_with_frontend_layout('dashboard.html')


@app.route("/my_photos")
@login_required
def my_photos():
    return render_template_with_frontend_layout('my_photos.html')


@app.route("/orders")
@login_required
def orders():
    return render_template_with_frontend_layout('orders.html')


@app.route("/messages")
@login_required
def messages():
    return render_template_with_frontend_layout('messages.html')


@app.route("/settings")
@login_required
def settings():
    return render_template_with_frontend_layout('settings.html')
