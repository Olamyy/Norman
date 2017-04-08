from flask import render_template, Blueprint, redirect

from flask_login import login_required

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard/admin/dashboard.html')


@blueprint.route('/logout', methods=['GET'])
def logout():
    return redirect('auth')


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