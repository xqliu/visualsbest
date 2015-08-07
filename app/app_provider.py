# coding=utf-8
class AppInfo(object):

    # 头像上传存储的服务
    _galleries_store_service = None
    # Flask App的引用
    _app = None
    # SQLAlchemy 的 DB实例
    _db = None
    # Flask-Admin的Admin实例
    _admin = None

    def __init__(self):
        pass

    @staticmethod
    def get_app():
        return AppInfo._app

    @staticmethod
    def set_app(app):
        AppInfo._app = app

    @staticmethod
    def set_db(db):
        AppInfo._db = db

    @staticmethod
    def get_db():
        return AppInfo._db

    @staticmethod
    def set_admin(admin):
        AppInfo._admin = admin

    @staticmethod
    def get_admin():
        return AppInfo._admin

    @staticmethod
    def set_galleries_store_service(galleries_upload_set):
        AppInfo._galleries_store_service = galleries_upload_set

    @staticmethod
    def get_galleries_store_service():
        return AppInfo._galleries_store_service
