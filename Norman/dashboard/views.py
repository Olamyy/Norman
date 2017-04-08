from flask import render_template, Blueprint, redirect

from flask_login import login_required

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard/admin/dashboard.html')


@blueprint.route('/create-user', methods=['GET'])
def create_user():
    return render_template('dashboard/admin/create-user.html')


@blueprint.route('/view-users', methods=['GET'])
def view_users():
    return render_template('dashboard/admin/view-users.html')


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