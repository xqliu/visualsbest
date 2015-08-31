# coding=utf-8
from datetime import datetime
from app import AppInfo, const
from app.models import PhotoWork, Image, EnumValues, PhotoCollection
from app.util import view_util
from app.util.view_util import rt
from flask import request
from sqlalchemy import or_


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
            PhotoWork.query.filter_by(id=work_id).delete()
            Image.query.filter_by(id=work.image.id).delete()


def save_photo_collection(form, photo_collection):
    photo_collection.category_id = int(form.category.data)
    photo_collection.style_id = int(form.style.data)
    photo_collection.name = form.name.data
    photo_collection.introduce = form.introduce.data
    photo_collection.price = form.price.data


def query_for_photo_collection(category_id, include_none_date, include_none_price,
                               max_date, max_price, min_date, min_price, style_id):
    """
    通过一组条件查询作品集
    :param category_id: 作品的分类id
    :param style_id: 作品的风格id
    :param include_none_date:是否包括日期为空的记录
    :param include_none_price:是否包括价格为空的记录
    :param max_date:最大的作品日期
    :param max_price: 最大的价格
    :param min_date: 最小的作品日期
    :param min_price: 最小的日期
    :return: 查询到的作品集的列表，查询条件的作品分类，查询条件的作品风格
    """
    query = AppInfo.get_db().session.query(PhotoCollection)
    category, style = None, None
    if category_id is not None:
        query = query.filter(PhotoCollection.category_id == category_id)
        category = EnumValues.query.get(category_id)
    if style_id is not None:
        query = query.filter(PhotoCollection.style_id == style_id)
        style = EnumValues.query.get(style_id)
    if min_price is not None:
        if include_none_price:
            query = query.filter(or_(PhotoCollection.price >= min_price, PhotoCollection.price.is_(None)))
        else:
            query = query.filter(PhotoCollection.price >= min_price)
    if max_price is not None:
        if include_none_price:
            query = query.filter(or_(PhotoCollection.price <= max_price, PhotoCollection.price.is_(None)))
        else:
            query = query.filter(PhotoCollection.price <= max_price)
    if min_date is not None:
        if include_none_date:
            query = query.filter(or_(PhotoCollection.date >= min_date, PhotoCollection.date.is_(None)))
        else:
            query = query.filter(PhotoCollection.date >= min_date)
    if max_date is not None:
        if include_none_date:
            query = query.filter(or_(PhotoCollection.date <= max_date, PhotoCollection.date.is_(None)))
        else:
            query = query.filter(PhotoCollection.date <= max_date)
    collections = query.filter(PhotoCollection.photos.any()).all()
    return collections, category, style


def extra_fields_from_form():
    """
    从request中获取用户输入的查询条件各字段
    :return: 查询的作品分类id、是否包含无日期的、是否包含无价格的、最大日期、最大价格、最小日期、最小价格、查询的作品风格id
    """
    category_id = int(request.form.get('category_id')) if len(request.form.get('category_id')) > 0 else None
    style_id = int(request.form.get('style_id')) if len(request.form.get('style_id')) > 0 else None
    min_price = int(request.form.get('min_price')) if len(request.form.get('min_price')) > 0 else None
    max_price = int(request.form.get('max_price')) if len(request.form.get('max_price')) > 0 else None
    min_date = datetime.strptime(request.form.get('min_date'), '%Y-%m-%d') \
        if len(request.form.get('min_date')) > 0 else None
    max_date = datetime.strptime(request.form.get('max_date'), '%Y-%m-%d') \
        if len(request.form.get('max_date')) > 0 else None
    include_none_price = request.form.get('include_none_price')
    include_none_date = request.form.get('include_none_date')
    return category_id, include_none_date, include_none_price, max_date, max_price, min_date, min_price, style_id


def render_search_result(template, router, get_all, get_filtered):
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    category, style, include_none_date, include_none_price, min_price, max_price, min_date, max_date = \
        [None, None, None, None, None, None, None, None]
    if request.method == 'POST':
        category_id, include_none_date, include_none_price, max_date, max_price, min_date, min_price, style_id = \
            extra_fields_from_form()
        collections, category, style = query_for_photo_collection(category_id, include_none_date, include_none_price,
                                                                  max_date, max_price, min_date, min_price, style_id)
        min_date = request.form.get('min_date')
        max_date = request.form.get('max_date')
        result_list = get_filtered(collections)
    else:
        result_list = get_all()
    return rt(template, result_list=result_list, categories=categories,
                                        styles=styles, category=category, style=style, route=router,
                                        min_price=min_price, max_price=max_price, include_none_price=include_none_price,
                                        min_date=min_date, max_date=max_date, include_none_date=include_none_date)
