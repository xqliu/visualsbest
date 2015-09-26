from datetime import datetime

from app import const, AppInfo
from app.models import Message, EnumValues
from flask import render_template

app = AppInfo.get_app()
db = AppInfo.get_db()


def create_request_msg(from_user_id, to_user_id, template_file, render_obj):
    content = render_template(template_file, request=render_obj)
    message = create_message(from_user_id, to_user_id, content)
    db.session.add(message)


def create_message(from_user_id, to_user_id, content):
    message = Message()
    message.from_user_id = from_user_id
    message.receive_user_id = to_user_id
    message.date = datetime.now()
    message.content = content
    status = EnumValues.find_one_by_code(const.MESSAGE_STATUS_UNREAD)
    message.status_id = status.id
    return message
    # TODO: Send EMail to receive_user
