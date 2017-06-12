from flask import render_template, Blueprint, redirect, jsonify
from flask import request
from flask import url_for

from Norman.auth.auth_utils import HospitalUtil, ServiceUtil, PatientUtil
from Norman.auth.forms import LoginForm, VerificationForm
from Norman.settings import ErrorConfig
from Norman.utils import validate_hashes

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='../static')

hospitalObj = HospitalUtil()
serviceObj = ServiceUtil()
userObj = PatientUtil()


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    action = request.args.get('action')
    error = ""
    if action == "invalidRoute":
        error = ErrorConfig.INVALID_ROUTE_ERROR
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        hospital_user = hospitalObj.validate_email(email)
        if hospital_user and validate_hashes(request.form["password"],
                                             hospital_user.password) and hospital_user.is_active:
            if hospitalObj.login_user_updates(hospital_user.id):
                hospitalObj.write_to_session('current_user', str(hospital_user))
                return redirect(url_for('dashboard.dashboard'))
            else:
                return render_template('dashboard/admin/login.html', error=ErrorConfig.INVALID_LOGIN_ERROR, form=form)
        else:
            return render_template('dashboard/admin/login.html', error=ErrorConfig.INVALID_LOGIN_ERROR, form=form)
    return render_template('dashboard/admin/login.html', form=form, error=error)


@blueprint.route('/hospital', methods=['GET', 'POST'])
def dashboard():
    hospital = hospitalObj.get_current_user_instance()
    if not hospital.active:
        return redirect(url_for('dashboard.verify'))
    return render_template('dashboard/admin/dashboard.html', hospital=hospital)


@blueprint.route('/logout', methods=['GET'])
def logout():
    hospital = hospitalObj.get_current_user_instance()
    hospitalObj.logout_user_updates(hospital.tempID)
    return redirect(url_for('dashboard.login'))


@blueprint.route('/profile', methods=['GET'])
def profile():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/profile.html', hospital=hospital)


@blueprint.route('/view-hospital-profile', methods=['GET'])
def view_hospital_profile():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/view-hospital-profile.html', hospital=hospital)


@blueprint.route('/edit-hospital-profile', methods=['GET'])
def edit_hospital_profile():
    hospital = hospitalObj.get_current_user_instance()
    service_list = serviceObj.get_all_services()
    return render_template('dashboard/admin/edit-hospital-profile.html', hospital=hospital, services=service_list)


@blueprint.route('/view-services', methods=['GET'])
def view_services():
    hospital = hospitalObj.get_current_user_instance()
    service_list = serviceObj.get_all_services()
    return render_template('dashboard/admin/view-services.html', hospital=hospital, services=service_list)


@blueprint.route('/choose-services', methods=['GET'])
def choose_services():
    hospital = hospitalObj.get_current_user_instance()
    service_list = serviceObj.get_all_services()
    return render_template('dashboard/admin/choose-services.html', hospital=hospital, services=service_list)


@blueprint.route('/service-info', methods=['GET'])
def service_info():
    hospital = hospitalObj.get_current_user_instance()
    service_list = serviceObj.get_all_services()
    return render_template('dashboard/admin/choose-services.html', hospital=hospital, services=service_list)


@blueprint.route('/edit-services', methods=['GET'])
def edit_services():
    hospital = hospitalObj.get_current_user_instance()
    service_list = serviceObj.get_all_services()
    return render_template('dashboard/admin/view-services.html', hospital=hospital, services=service_list)


@blueprint.route('/request-service', methods=['GET', 'POST'])
def request_service():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/request-service.html', hospital=hospital)


@blueprint.route('/add-patient', methods=['GET'])
def add_patient():
    hospital = hospitalObj.get_current_user_instance()
    service_list = serviceObj.get_all_services()
    return render_template('dashboard/admin/add-patient.html', hospital=hospital, services=service_list)


@blueprint.route('/view-patients', methods=['GET'])
def view_patients():
    hospital = hospitalObj.get_current_user_instance()
    patient_list = hospitalObj.get_all_patients(hospital.hospital_id)
    return render_template('dashboard/admin/view-patient.html', hospital=hospital, patient_list=patient_list)


@blueprint.route('/patient', methods=['GET'])
def patient():
    patient_id = request.args.get('pID')
    hospital = hospitalObj.get_current_user_instance()
    if patient_id:
        patient_data = userObj.get_by_userID(patient_id)
        return render_template('dashboard/admin/single-patient.html', hospital=hospital, patient_data=patient_data)
    return render_template('dashboard/admin/single-patient.html', hospital=hospital)


@blueprint.route('/edit-patient', methods=['GET'])
def edit_patient():
    patient_id = request.args.get('pID')
    hospital = hospitalObj.get_current_user_instance()
    if patient_id:
        patient_data = userObj.get_by_userID(patient_id)
        return render_template('dashboard/admin/edit-single-patient.html', hospital=hospital, patient_data=patient_data)
    return render_template('dashboard/admin/edit-single-patient.html', hospital=hospital)


@blueprint.route('/password-reset', methods=['GET'])
def password_reset():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/password-reset.html', hospital=hospital)


@blueprint.route('/verify', methods=['GET', 'POST'])
def verify():
    hospital = hospitalObj.get_current_user_instance()
    if hospital:
        form = VerificationForm(request.form)
        if request.method == "POST":
            verificationID = request.form['verificationCode']
            if hospital.get_by_verID(verificationID):
                hospital.update_active(verificationID)
                return redirect(url_for('dashboard.dashboard'))
            else:
                return render_template('dashboard/admin/verify.html', hospital=hospital,
                                       error=ErrorConfig.INVALID_VER_ID_ERROR, form=form)
        return render_template('dashboard/admin/verify.html', hospital=hospital, form=form)
    else:
        return redirect(url_for('dashboard.login', action="invalidRoute"))


@blueprint.route('/records', methods=['GET'])
def records():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/records.html', hospital=hospital)


@blueprint.route('/patient-settings', methods=['GET'])
def patient_settings():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/patient-settings.html', hospital=hospital)


@blueprint.route('/security-settings', methods=['GET'])
def security_settings():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/security-settings.html', hospital=hospital)


@blueprint.route('/user-profile', methods=['GET'])
def user_profile():
    patient_id = request.args.get('pID')
    hospital = hospitalObj.get_current_user_instance()
    if patient_id:
        patient_data = userObj.get_by_userID(patient_id)
        return render_template('dashboard/admin/user-profile.html', hospital=hospital, patient_data=patient_data)
    return render_template('dashboard/admin/user-profile.html', hospital=hospital)


@blueprint.route('/edit-user-profile', methods=['GET'])
def edit_user_profile():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/edit-user-profile.html', hospital=hospital)


@blueprint.route('/confirm-email', methods=['GET'])
def confirm_email():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/confirm-email.html', hospital=hospital)


@blueprint.route('/success-email', methods=['GET'])
def success_email():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/success-email.html', hospital=hospital)


@blueprint.route('/service-notification-email', methods=['GET'])
def service_notification_email():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/service-notification-email.html', hospital=hospital)


@blueprint.route('/password-reset-email', methods=['GET'])
def password_reset_email():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/password-reset-email.html', hospital=hospital)


@blueprint.route('/password-choosing-email', methods=['GET'])
def password_choosing_email():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/password-choosing-email.html', hospital=hospital)


@blueprint.route('/added-patient-email', methods=['GET'])
def added_patient_email():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/added-patient-email.html', hospital=hospital)


@blueprint.route('/password-recovery-email', methods=['GET'])
def password_recovery_email():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/password-recovery-email.html', hospital=hospital)


@blueprint.route('/patient-dashboard', methods=['GET'])
def patient_dashboard():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/patient-dashboard.html', hospital=hospital)


@blueprint.route('/patient-password-choosing', methods=['GET'])
def patient_password_choosing():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/patient-password-choosing.html', hospital=hospital)


@blueprint.route('/patient-messages', methods=['GET'])
def patient_messages():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/patient-messages.html', hospital=hospital)


@blueprint.route('/single-patient-message', methods=['GET'])
def single_patient_message():
    hospital = hospitalObj.get_current_user_instance()
    return render_template('dashboard/admin/single-patient-message.html', hospital=hospital)
