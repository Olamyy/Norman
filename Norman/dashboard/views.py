from flask import render_template, Blueprint, redirect


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
