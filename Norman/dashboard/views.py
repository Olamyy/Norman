from flask import render_template, Blueprint, redirect, jsonify
from flask import request
from flask import url_for
from Norman.auth.auth_utils import HospitalUtil
from Norman.auth.forms import LoginForm
from Norman.settings import ErrorConfig
from Norman.utils import validate_hashes

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='../static')

hospitalObj = HospitalUtil()


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        hospital_user = hospitalObj.validate_email(email)
        if hospital_user and validate_hashes(request.form["password"], hospital_user.password) and hospital_user.is_active:
            if hospitalObj.login_user_updates(hospital_user.id):
                return redirect(url_for('dashboard.dashboard', verID=hospital_user.tempID))
            else:
                return render_template('dashboard/admin/login.html', error=ErrorConfig.INVALID_LOGIN_ERROR, form=form)
        else:
            return render_template('dashboard/admin/login.html', error=ErrorConfig.INVALID_LOGIN_ERROR, form=form)
    return render_template('dashboard/admin/login.html', form=form)


@blueprint.route('/hospital', methods=['GET', 'POST'])
def dashboard():
    verification_id = request.args.get('verID')
    hospital = hospitalObj.get_by_verID(verification_id)
    return render_template('dashboard/admin/dashboard.html', hospital=hospital)


@blueprint.route('/logout', methods=['GET'])
def logout():
    verID = request.args.get('verID')
    hospitalObj.logout_user_updates(verID)
    return redirect(url_for('dashboard.login'))


@blueprint.route('/profile', methods=['GET'])
def profile():
    return render_template('dashboard/admin/profile.html')


@blueprint.route('/view-hospital-profile', methods=['GET'])
def view_hospital_profile():
    return render_template('dashboard/admin/view-hospital-profile.html')


@blueprint.route('/edit-hospital-profile', methods=['GET'])
def edit_hospital_profile():
    return render_template('dashboard/admin/edit-hospital-profile.html')


@blueprint.route('/view-services', methods=['GET'])
def view_services():
    return  render_template('dashboard/admin/view-services.html')


@blueprint.route('/add-patient', methods=['GET'])
def add_patient():
    return render_template('dashboard/admin/add-patient.html')


@blueprint.route('/view-patients', methods=['GET'])
def view_patients():
    return render_template('dashboard/admin/view-patient.html')


@blueprint.route('/patient', methods=['GET'])
def patient():
    return render_template('dashboard/admin/single-patient.html')


@blueprint.route('/password-reset', methods=['GET'])
def password_reset():
    return render_template('dashboard/admin/password-reset.html')


@blueprint.route('/verify', methods=['GET'])
def verify():
    verification_id = request.args.get('verID')
    hospital = hospitalObj.get_by_verID(verification_id)
    if hospital:
        return render_template('dashboard/admin/verify.html', hospital=hospital)
    else:
        return redirect(url_for('dashboard.login'))
