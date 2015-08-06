from app import AppInfo


def save_obj_commit(obj):
    AppInfo.get_db().session.add(obj)
    AppInfo.get_db().session.commit()