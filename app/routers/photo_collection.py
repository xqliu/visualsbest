# encoding=utf-8
from app import app_provider, AppInfo, const
from app.forms.photo_collection_form import PhotoCollectionForm
from app.models import EnumValues, \
    PhotoCollection
from app.util.db_util import save_obj_commit, delete_by_id
from app.util.photo_collection_util import add_photo_works, delete_photo_works, save_photo_collection
from app.util.view_util import rt
from flask import request, redirect, url_for, flash
from flask.ext.login import current_user
from flask.ext.security import login_required

app = app_provider.AppInfo.get_app()


@app.route("/collection_details/<int:collection_id>")
def collection_details(collection_id):
    collection = PhotoCollection.query.get(collection_id)
    return rt('collection_details.html', collection=collection)


@app.route("/edit_collection/<int:collection_id>", methods=['GET', 'POST'])
def edit_collection(collection_id):
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection.query.get(collection_id)
    if photo_collection.photographer != current_user:
        flash('您没有权限编辑本作品集，将返回网站主页')
        return redirect(url_for('index'))
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        if request.form.get('photo-collection-to-delete') is not None \
                and len(request.form.get('photo-collection-to-delete')) != 0:
            id_to_delete = int(request.form.get('photo-collection-to-delete'))
            delete_by_id(PhotoCollection, id_to_delete)
            flash('作品集删除成功')
            return redirect(url_for('my_photos'))
        elif request.form.get('photo-works-to-delete') is not None:
            works_to_delete = request.form.get('photo-works-to-delete').split(',')
            delete_photo_works(works_to_delete)
            files = request.files.getlist('photos[]')
            if not (len(files) == 1 and files[0].filename == u''):
                add_photo_works(files, photo_collection)
        else:
            save_photo_collection(form, photo_collection)
        AppInfo.get_db().session.commit()
    return rt('edit_collection.html', photo_collection=photo_collection, categories=categories, form=form,
              styles=styles)


@app.route("/create_collection", methods=['GET', 'POST'])
@login_required
def create_collection():
    categories = EnumValues.type_filter(const.PHOTO_CATEGORY_KEY).all()
    styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
    photo_collection = PhotoCollection()
    form = PhotoCollectionForm(categories, styles)
    if request.method == 'POST':
        if form.validate_on_submit():
            photo_collection.photographer_id = current_user.id
            photo_collection.uploader_id = current_user.id
            save_photo_collection(form, photo_collection)
            save_obj_commit(photo_collection)
            flash('作品集创建成功，您可以在本界面上传作品集中的作品')
            return redirect(url_for('edit_collection', collection_id=photo_collection.id))
        else:
            flash('请填写所有信息并再次尝试创建')
    return rt('create_collection.html', photo_collection=photo_collection, categories=categories, form=form,
              styles=styles)
