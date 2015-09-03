# encoding=utf-8
from app import app_provider
from app.forms.user_profile_form import UserProfileForm
from app.models import User, UserExperience
from app.util.db_util import save_obj_commit
from app.util.view_util import rt
from flask import request, redirect, url_for, flash
from flask.ext.login import current_user
from flask.ext.security import login_required

app = app_provider.AppInfo.get_app()


@app.route('/experience/edit/<int:photographer_id>', methods=['GET', 'POST'])
@login_required
def edit_experience(photographer_id):
    if photographer_id == current_user.id:
        user = User.query.filter_by(id=photographer_id).first()
        exp = user.experience
        if request.method == 'POST':
            if exp is None:
                exp = UserExperience()
            exp.user_id = user.id
            exp.content = request.form['experience-textarea']
            save_obj_commit(exp)
        return rt('edit_experience.html', user_profile_form=UserProfileForm(), experience=exp)
    else:
        flash('您没有权限编辑该用户的摄影经历')
        return redirect(url_for('index'))


@app.route('/experience/<int:photographer_id>', methods=['GET'])
def experience(photographer_id):
    user = User.query.filter_by(id=photographer_id).first()
    exp = user.experience
    return rt('experience.html', user_profile_form=UserProfileForm(), photographer=user, experience=exp)
