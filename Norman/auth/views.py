# -*- coding: utf-8 -*-


from flask import Blueprint, render_template

blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def auth():
    return render_template('dashboard/admin/register.html')


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('dashboard/admin/login.html')


@blueprint.route('/register/hospital', methods=['GET'])
def hospital_reg():
    return render_template('auth/registerhospital.html')


# FOR SELECTION OF PLAN ID AFTER REGISTRATION
@blueprint.route('/plans', methods=['GET'])
def plan():
    return render_template('dashboard/admin/plans.html')
