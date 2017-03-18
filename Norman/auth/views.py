# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask import request
from Norman.hospital.models import Hospital
from Norman.hospital.forms import RegisterForm
from Norman.utils import flash_errors

blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def auth():
        return render_template('auth/auth.html')


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')


@blueprint.route('/register/hospital', methods=['GET'])
def hospital_reg():
    return render_template('auth/registerhospital.html')

