# encoding=utf-8
from app import app_provider, AppInfo
from app.models import EnumValues, \
    Message
from app.util.db_util import save_obj_commit
from app.util.view_util import rt
from flask import request, redirect, url_for, flash
from flask.ext.login import current_user
from flask.ext.security import login_required
from app.const import MESSAGE_STATUS_READ

app = app_provider.AppInfo.get_app()
db = AppInfo.get_db()


@app.route("/messages/")
@app.route("/messages/<status_code>")
@login_required
def messages(status_code='unread'):
    msgs = db.session.query(Message).outerjoin(EnumValues, Message.status) \
        .filter(EnumValues.code == "MESSAGE_STATUS_" + status_code.upper()).filter(
        Message.receive_user_id == current_user.id).order_by(Message.date.desc()).all()
    return rt('messages.html', messages=msgs)


@app.route('/message/<msg_id>', methods=['GET'])
@login_required
def message(msg_id):
    msg = Message.query.get(msg_id)
    status = EnumValues.find_one_by_code(MESSAGE_STATUS_READ)
    msg.status = status
    save_obj_commit(msg)
    return rt('message.html', message=msg)


@app.route('/message/process', methods=['POST'])
@login_required
def process_message():
    operation = request.form.get('operation')
    message_id = int(request.form.get('message_id'))
    msg = Message.query.get(message_id)
    if operation == 'read':
        if msg.receive_user_id == current_user.id:
            status = EnumValues.find_one_by_code(MESSAGE_STATUS_READ)
            msg.status = status
            save_obj_commit(msg)
        else:
            flash("标记消息已读成功")
    return redirect(url_for('messages'))
