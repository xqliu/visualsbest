from datetime import datetime
from app import const

from app.models import Message, EnumValues
from app.util.db_util import save_obj_commit


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
