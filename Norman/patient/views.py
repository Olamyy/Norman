from flask import render_template, Blueprint, redirect, jsonify
from flask import request
from flask import url_for

from Norman.auth.auth_utils import PatientUtil, ServiceUtil
from Norman.auth.forms import PatientLoginForm, PatientPasswordChooseForm
from Norman.settings import ErrorConfig
from Norman.utils import validate_hashes

blueprint = Blueprint('user', __name__, url_prefix='/dashboard/user', static_folder='../static')

userObj = PatientUtil()
serviceObj = ServiceUtil()


@blueprint.route('/', methods=['GET', 'POST'])
def dashboard():
    user_id, coming_from = request.args.get('user-id'), request.args.get('coming-from')
    if not user_id and not coming_from:
        return redirect(url_for('user.login', action="invalidRoute"))
    else:
        user_id = userObj.get_by_user_id(user_id)
        if user_id:
            if user_id.has_chosen_password:
                return render_template('dashboard/patient/dashboard.html', user=user_id)
            else:
                return redirect(url_for('user.password_chooser', user_id=user_id))
        else:
            return redirect(url_for('user.login', action="somethingWrong"))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = PatientLoginForm(request.form)
    action = request.args.get('action')
    error = ErrorConfig.get_error_by_code(action) if action else None
    if request.method == "POST" and "email" in request.form:
            email = request.form["email"]
            patient = userObj.validate_email(email)
            if patient and validate_hashes(request.form["password"], patient.password) and patient.is_active:
                if userObj.login_user_updates(patient.id):
                    userObj.write_to_session('current_user', str(patient))
                    return redirect(url_for('dashboard.dashboard'))
                else:
                    return render_template('dashboard/patient/login.html', error=ErrorConfig.INVALID_LOGIN_ERROR, form=form)
            else:
                return render_template('dashboard/patient/login.html', error=ErrorConfig.INVALID_LOGIN_ERROR, form=form)
    return render_template('dashboard/patient/login.html', form=form, error=error)


@blueprint.route('/choose-password', methods=['GET', 'POST'])
def password_chooser():
    form = PatientPasswordChooseForm(request.form)
    user_id = request.args.get('user_id')
    if request.method == "POST" and "password" in request.form:
        password = request.form["passsword"]
        patient = userObj.get_by_id(user_id)
        if patient:
            userObj.update_password(user_id, password)
            if userObj.update_password(user_id, password):
                userObj.choose_password_updates(patient.id)
                userObj.write_to_session('current_user', str(patient))
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('dashboard.login', action="UnableToSetPassword"))
        else:
            return render_template('dashboard/admin/login.html', error=ErrorConfig.INVALID_ID_ERROR, form=form)
    return render_template('dashboard/patient/choose_password.html', form=form)
