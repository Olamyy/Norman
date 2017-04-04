# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request, abort, jsonify
from Norman.models import Hospital
from mongoengine.errors import DoesNotExist
from Norman.auth.forms import LoginForm
from Norman.auth.auth_utils import HospitalUtil
from Norman.utils import  validate_hashes
from flask_login import login_user, logout_user, login_manager
import chatterbot

blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def auth():
    return redirect(url_for('auth.register'))


@blueprint.route('/hospital/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        hospitalObj = HospitalUtil()
        user = hospitalObj.get_by_email_w_password(email)
        if user and validate_hashes(request.form["password"], user.password) and user.is_active:
            remember = request.form.get("remember", "n") == "y"
            if login_user(user, remember=remember):
                return redirect('/')
            else:
                error = "Invalid Details"
                return render_template('dashboard/admin/login.html', error=error, form=form)
        else:
            return jsonify({'Here': request.form})
    return render_template('dashboard/admin/login.html', form=form)


@blueprint.route('/hospital/register', methods=['GET'])
def register():
    action, verification_id = request.args.get('action'), request.args.get('verID')
    if action:
        if action == "verify":
            return redirect(url_for('auth.verify', action=action, verID=verification_id))
    return render_template('dashboard/admin/register.html')


@blueprint.route('/hospital/register/plans', methods=['GET'])
def plan():
    return render_template('dashboard/admin/plans.html')


@blueprint.route('/hospital/verify', methods=['GET'])
def verify():
    verification_id = request.args.get('verID')
    try:
        hospital = Hospital.objects.get(ver_id=verification_id)
        return render_template('dashboard/admin/verify.html', hospital=hospital)
    except DoesNotExist as error:
        return abort(404)
