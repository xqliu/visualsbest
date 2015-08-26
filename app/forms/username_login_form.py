# encoding=utf-8
from flask.ext.security import LoginForm
from flask.ext.security.confirmable import requires_confirmation
from flask.ext.security.forms import get_form_field_label, _datastore
from flask.ext.security.utils import get_message, verify_and_update_password
from wtforms import StringField, PasswordField


class UsernameLoginForm(LoginForm):
    login = StringField(get_form_field_label('login'))
    password = PasswordField(get_form_field_label('password'))

    def validate(self):
        if not super(UsernameLoginForm, self).validate():
            pass
        if self.login.data.strip() == '':
            self.login.errors.append(get_message('LOGIN_NOT_PROVIDED')[0])
            return False

        if self.password.data.strip() == '':
            self.password.errors.append(get_message('PASSWORD_NOT_PROVIDED')[0])
            return False

        self.user = _datastore.find_user(login=self.login.data.strip())

        if self.user is None:
            self.login.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False
        if not self.user.password:
            self.password.errors.append(get_message('PASSWORD_NOT_SET')[0])
            return False
        if not verify_and_update_password(self.password.data, self.user):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        if requires_confirmation(self.user):
            self.login.errors.append(get_message('CONFIRMATION_REQUIRED')[0])
            return False
        if not self.user.is_active():
            self.login.errors.append(get_message('DISABLED_ACCOUNT')[0])
            return False
        return True
