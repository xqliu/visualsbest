from app import AppInfo


def save_obj_commit(obj):
    AppInfo.get_db().session.add(obj)
    AppInfo.get_db().session.commit()


def delete_by_id(obj_type, id_to_del):
    """
    :type obj_type: db.Model
    :type id_to_del: int
    """
    obj = obj_type.query.get(id_to_del)
    AppInfo.get_db().session.delete(obj)
    AppInfo.get_db().session.commit()