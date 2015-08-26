# coding=utf-8
from app import AppInfo
from app.models import PhotoWork, Image, EnumValues
from app.util import view_util


def add_photo_works(files, photo_collection):
    for img in files:
        work = PhotoWork()
        work.photo_collection_id = photo_collection.id
        view_util.save_photo_work_image(work, img)
        AppInfo.get_db().session.add(work)


def delete_photo_works(works_to_delete):
    if not (len(works_to_delete) == 1 and works_to_delete[0] == u''):
        for work_id in works_to_delete:
            work = PhotoWork.query.filter_by(id=int(work_id)).first()
            # 如果public_id不为空，说明是云端存储的，使用public_id删除
            # 如果public_id为空，说明是本地存储的，则使用image.py中定义的after_delete的监听器删除
            if work.image.public_id is not None:
                AppInfo.get_image_store_service().remove(work.image.public_id)
            PhotoWork.query.filter_by(id=work_id).delete()
            Image.query.filter_by(id=work.image.id).delete()


def save_photo_collection(form, photo_collection):
    photo_collection.category_id = int(form.category.data)
    photo_collection.style_id = int(form.style.data)
    photo_collection.name = form.name.data
    photo_collection.introduce = form.introduce.data
    photo_collection.price = form.price.data
