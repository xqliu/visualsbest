from app import AppInfo

db = AppInfo.get_db()


def save_objects_commit(*objects):
    """
    Save object and commit to database
    :param objects: Objects to save
    """
    for obj in objects:
        db.session.add(obj)
    db.session.commit()


def save_obj_commit(obj):
    db.session.add(obj)
    db.session.commit()


def delete_by_id(obj_type, id_to_del):
    """
    :type obj_type: db.Model
    :type id_to_del: int
    """
    obj = obj_type.query.get(id_to_del)
    AppInfo.get_db().session.delete(obj)
    AppInfo.get_db().session.commit()
