# encoding=utf-8
import calendar
from datetime import date, timedelta

from app import app_provider, AppInfo
from app.const import DATE_STATUS_NOT_AVAILABLE
from app.forms.date_status_form import DateStatusForm
from app.models import User, EnumValues, \
    DateStatus
from app.util.db_util import save_obj_commit, delete_by_id
from app.util.view_util import rt
from flask import request, redirect, url_for, flash, jsonify
from flask.ext.login import current_user
from flask.ext.security import login_required
from sqlalchemy import or_, and_

app = app_provider.AppInfo.get_app()


@app.route('/date_status/json/<int:photographer_id>', methods=['GET'])
def date_status_json(photographer_id):
    year = int(request.args.get('ano'))
    month = int(request.args.get('mes'))
    month_begin = date(year, month, 1)
    month_end = date(year, month, calendar.monthrange(year, month)[1])
    query = AppInfo.get_db().session.query(DateStatus)
    date_statuses = query.filter(DateStatus.user_id == photographer_id) \
        .filter(or_(and_(DateStatus.start_date >= month_begin, DateStatus.start_date <= month_end),
                    and_(DateStatus.end_date >= month_begin, DateStatus.end_date <= month_end))).all()
    events = []
    for ds in date_statuses:
        day_count = (ds.end_date - ds.start_date).days + 1
        for single_date in [d for d in (ds.start_date + timedelta(n) for n in range(day_count)) if d <= ds.end_date]:
            event = dict()
            event['date'] = '{dt.day}/{dt.month}/{dt.year}'.format(dt=single_date)
            event['title'] = u'不可用'
            event['color'] = u'rgba(190, 190, 190, 0.6)'
            event['class'] = u'unavailable'
            events.append(event)
    return jsonify(events=events)


@app.route('/date_status/edit/<int:photographer_id>', methods=['GET', 'POST'])
@login_required
def edit_date_status(photographer_id):
    if photographer_id == current_user.id:
        user = User.query.filter_by(id=photographer_id).first()
        form = DateStatusForm()
        if request.method == 'POST':
            if request.form.get('action') == 'create':
                if form.validate_on_submit():
                    start_date = form.from_day.data
                    end_date = form.end_day.data
                    date_status = DateStatus()
                    date_status.start_date = start_date
                    date_status.end_date = end_date
                    date_status.user_id = photographer_id
                    date_status.status = EnumValues.find_one_by_code(DATE_STATUS_NOT_AVAILABLE)
                    save_obj_commit(date_status)
                    flash('工作日历修改成功')
                else:
                    flash('输入错误，请重新选择起始日期')
            elif request.form.get('action') == 'delete':
                id_to_del = int(request.form.get('id_to_delete'))
                delete_by_id(DateStatus, id_to_del)
                flash('工作日历中不可用时间段删除成功')
        date_statuses = user.date_statuses
        return rt('edit_date_status.html', form=form, date_statuses=date_statuses)
    else:
        flash('您没有权限编辑该用户的工作日历')
        return redirect(url_for('index'))
