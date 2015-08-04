# coding=utf-8
from flask.ext.babelex import lazy_gettext
from base_view import ModelViewWithAccess
from flask.ext.security.utils import encrypt_password
from wtforms import PasswordField


# Customized User model for SQL-Admin
class UserAdmin(ModelViewWithAccess):
    # Don't display the password on the list of Users
    column_exclude_list = list = ('password',)

    column_list = ('id', 'login', 'display', 'email', 'type',
                   'status', 'active', 'confirmed_at',)

    column_editable_list = ('display', 'email', 'active')

    column_searchable_list = (
        'login', 'display', 'email', 'type.display', 'status.display')

    column_labels = dict(
        id=u'编号',
        login=u'登陆名',
        display=u'显示名称',
        email=u'电子邮箱',
        active=u'允许登陆系统?',
        roles=u'角色',
        type=u'用户类型',
        status=u'用户状态',
        confirmed_at=u'确认时间',
    )

    # Don't include the standard password field when creating or editing a
    # User (but see below)
    form_excluded_columns = ('password', 'image', 'recommend_by',
                             'sent_requests', 'received_requests',
                             'data_statuses', 'favourites', 'comments_created',
                             'photo_categories',
                             'experience', 'recommended_users',
                             'produced_photo_collections',
                             'uploaded_photo_collections', 'sent_messages',
                             'received_messages')

    form_edit_rules = ('login', 'display', 'email', 'type',
                       'status', 'password2', 'active')

    form_create_rules = form_edit_rules

    form_args = dict(
        active=dict(description=u'如果取消选中状态则禁止该用户登陆'),
    )

    # Automatically display human-readable names for the current and available
    # Roles when creating or editing a User
    column_auto_select_related = True

    # On the form for creating or editing a User, don't display a field
    # corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt
    # the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a
    # regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin.
        # We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New
        # Password".
        form_class.password2 = PasswordField(
            label=u'密码',
            description=lazy_gettext('如果不修改密码请留空'))
        return form_class

    # This callback executes when the user saves changes to a newly-created or
    # edited User -- before the changes are committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):
            # ... then encrypt the new password prior to storing it in the
            # database. If the password field is blank, the existing password
            # in the database will be retained.
            model.password = encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(ModelViewWithAccess):
    # Prevent administration of Roles unless the currently logged-in user has
    # the "admin" role
    column_list = ('id', 'name', 'description',)
    column_searchable_list = ('name', 'description')
    column_labels = dict(
        id=u'编号',
        name=u'名称',
        description=u'描述',
        users=u'该角色下的用户'
    )
    column_editable_list = ('description',)
